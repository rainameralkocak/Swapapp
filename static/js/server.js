const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3001;

app.use(bodyParser.json());
app.use(express.static('public'));

const busyDays = [3, 5, 10, 15]; // Eğitmenin meşgul olduğu günler
const availableDays = [2, 4, 6, 7, 11, 14, 16]; // Eğitmenin müsait olduğu günler
const timeSlots = ['09:00 - 10:00', '10:00 - 11:00', '11:00 - 12:00', '13:00 - 14:00', '14:00 - 15:00', '15:00 - 16:00', '16:00 - 17:00'];

app.get('/schedule', (req, res) => {
    res.json({ busyDays, availableDays, timeSlots });
});

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/profile.html');
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
