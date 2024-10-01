var brightness = msg.payload.light || null;
var CurrentBrightness

if (brightness !== null && brightness > 2 || brightness == 0) {
    CurrentBrightness = brightness;
    return { payload: brightness };  // ส่งความสว่างของไฟไปยัง Dashboard
}
else if (brightness == 1 ) {
    return { payload: 0 };
}else if (brightness == 2) {
    return {payload: CurrentBrightness || 100}
}

return null;