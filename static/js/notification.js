// ==========================================
// NOTIFICATIONS
// ==========================================

function showNotification(

    title,
    message,
    type = "info"

) {

    const notification =
        document.createElement(
            "div"
        );

    notification.className =
        `os-notification ${type}`;

    notification.innerHTML =
        `
        <strong>${title}</strong>
        <br>
        ${message}
        `;

    document.body.appendChild(
        notification
    );

    setTimeout(
        () => {

            notification.remove();

        },
        5000
    );
}