// API Configuration - works with both local and production
const API_BASE = window.location.origin === 'http://localhost:3000' 
  ? 'http://localhost:8000' 
  : window.location.origin;

let currentTicket = null;

async function generateTicket()
{
    try {
        let response =
        await fetch(
        API_BASE + "/generate_ticket"
        );

        let data =
        await response.json();

        currentTicket = data.ticket;

        document
        .getElementById("ticketText")
        .innerHTML =
        "Ticket: " + currentTicket;
    } catch(error) {
        console.error("Error generating ticket:", error);
        alert("Failed to generate ticket. Check console for details.");
    }
}

async function generateQR()
{
    let slot =
    document
    .getElementById("slotInput")
    .value;

    if(currentTicket == null)
    {
        alert(
        "Generate Ticket First"
        );

        return;
    }

    let url =
    API_BASE + "/generate_qr/"
    + slot + "/"
    + currentTicket;

    document
    .getElementById("qrImage")
    .src = url;
}

async function loadDashboard()
{
    try {
        let response =
        await fetch(
        API_BASE + "/dashboard"
        );

        let data =
        await response.json();

        for(let i=0;i<6;i++)
        {
            let slotDiv =
            document.getElementById(
            "slot"+i
            );

            slotDiv.className =
            "slot free";
        }

        if(Array.isArray(data)) {
            data.forEach(row =>
            {
                if(row.active == 1)
                {
                    let slotDiv =
                    document.getElementById(
                    "slot"+row.slot
                    );

                    slotDiv.className =
                    "slot occupied";
                }
            });
        }
    } catch(error) {
        console.error("Error loading dashboard:", error);
    }
}

setInterval(
loadDashboard,
3000
);
