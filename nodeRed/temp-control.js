var temperature = msg.payload.condi || null;
var CurrentTemp = flow.get('CurrentTemp') || 25;  // กำหนดค่าเริ่มต้นเป็น 25

if (temperature === 3) {
    CurrentTemp += 1;
    flow.set('CurrentTemp', CurrentTemp);  // เก็บค่า CurrentTemp ใน Flow Context
    return { payload: CurrentTemp };  // ส่ง +1 องศาไปยัง Dashboard
} else if (temperature === 4) {
    CurrentTemp -= 1;
    flow.set('CurrentTemp', CurrentTemp);  // เก็บค่า CurrentTemp ใน Flow Context
    return { payload: CurrentTemp };  // ส่ง -1 องศาไปยัง Dashboard
} else if (temperature === 1) {
    return { payload: 'none' };
} else if (temperature === 2) {
    return { payload: CurrentTemp };
}

return null;