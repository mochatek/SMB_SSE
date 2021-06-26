const msgs = document.getElementById("msgs");

const eventSource = new EventSource("/notify");

eventSource.addEventListener("message", (event) => {
  const p = document.createElement("p");
  p.textContent = `${event.data}`;
  msgs.appendChild(p);
});

document
  .querySelector("#msg_form")
  .addEventListener("submit", async (event) => {
    event.preventDefault();

    const data = {
      to: this.to.value,
      msg: this.msg.value,
    };

    const response = await fetch("/send", {
      method: "POST",
      body: JSON.stringify(data),
      headers: { "content-type": "application/json" },
    });

    const { message_sent } = await response.json();
    if (!message_sent) {
      alert("Receiver is offline!");
    }
  });
