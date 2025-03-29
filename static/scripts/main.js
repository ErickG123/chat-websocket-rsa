const btnEncrypt = document.getElementById("btnEncrypt");
const btnDecrypt = document.getElementById("btnDecrypt");
const messageInput = document.getElementById("message");
let encryptedMessage = document.getElementById("encryptedMessage");

const chat = document.getElementById("chat");

const publicKey = document.getElementById("publicKey");
const privateKey = document.getElementById("privateKey");

const socket = io();

socket.on("connect", () => {
    console.log(`User Connected - Socket ID: ${socket.id}`);
});

btnEncrypt.addEventListener("click", () => {
    const data = {
        message: messageInput.value,
        publicKey: publicKey.value
    }

    socket.emit("encrypt_message", data);
});

socket.on("encryptedMessage", (encryptedMessage) => {
    chat.innerHTML += `
        <div class="border border-black rounded-md p-2.5 mb-2.5">
            <p>${encryptedMessage}</p>
        </div>
    `;
});

btnDecrypt.addEventListener("click", () => {
    const data = {
        message: encryptedMessage.value,
        privateKey: privateKey.value
    }

    socket.emit("decrypt_message", data);
});

socket.on("decryptedMessage", (decryptedMessage) => {
    encryptedMessage.value = decryptedMessage;
});
