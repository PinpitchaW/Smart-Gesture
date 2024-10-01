var Con = msg.payload;
var Type = Math.floor(Con / 100);
var Cons = Con % 100;

// ฟังก์ชันสำหรับส่งข้อความหลังจากดีเลย์
function sendDelayedMessage(topic, payload, delay) {
    setTimeout(() => {
        node.send({ topic: topic, payload: payload });
    }, delay);
}

// ตัวแปรเก็บค่าที่จะแสดงบน Dashboard
var dashboardPayload = {};

// ตรวจสอบประเภทของค่าและส่งข้อมูลตามที่กำหนด
if (Type === 20) {
    if (Cons === 1) {  // off
        sendDelayedMessage("light", Cons, 5000);
        dashboardPayload.light = Cons;  // เก็บค่าเพื่อแสดงบน Dashboard
    } else if (Cons === 2) { // on
        sendDelayedMessage("light", Cons, 5000);
        dashboardPayload.light = Cons;  // เก็บค่าเพื่อแสดงบน Dashboard
    } else {
        sendDelayedMessage("light", Cons, 1000);
        dashboardPayload.light = Cons;  // เก็บค่าเพื่อแสดงบน Dashboard
    }
} else if (Type === 10) {
    sendDelayedMessage("Condi", Cons, 5000);
    dashboardPayload.condi = Cons;  // เก็บค่าเพื่อแสดงบน Dashboard
} 
else{
    return null;
}

// ส่งค่าที่แยกออกไปยัง Dashboard
node.send({ topic: "dashboard", payload: dashboardPayload });

// ส่งค่า msg กลับไปยัง node ถ้าจำเป็น
return null;