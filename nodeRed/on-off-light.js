var lightStatus = msg.payload.light || "unknown";

if (lightStatus === 1) {
    return { payload: "off" };  // ส่งไปที่ Dashboard แสดง "off" ของไฟ
} else if (lightStatus === 2) {
    return { payload: "on" };   // ส่งไปที่ Dashboard แสดง "on" ของไฟ
}

return null; 