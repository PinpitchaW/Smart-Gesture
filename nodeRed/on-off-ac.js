var condiStatus = msg.payload.condi || "unknown";

if (condiStatus === 1) {
    return { payload: "off" };  // ส่งไปที่ Dashboard แสดง "off" ของแอร์
} else if (condiStatus === 2) {
    return { payload: "on" };   // ส่งไปที่ Dashboard แสดง "on" ของแอร์
}

return null;