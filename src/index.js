const express = require("express");
const path = require("path");
const app = express();
const hbs = require("hbs");
const LogInCollection = require("./mongodb");
const port = process.env.PORT || 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

const tempelatePath = path.join(__dirname, '../tempelates');
const publicPath = path.join(__dirname, '../public');
console.log(publicPath);

app.set('view engine', 'hbs');
app.set('views', tempelatePath);
app.use(express.static(publicPath));

app.get('/signup', (req, res) => {
    res.render('signup');
});
app.get('/contact',(req,res)=>{
    res.render('contact');
})
app.get('/', (req, res) => {
    res.render('login');
});
app.get('/about', (req, res) => {
    res.render('about');
});
app.get('/userm', (req, res) => {
    res.render('userm');
});
app.post('/signup', async (req, res) => {
    const data = {
        name: req.body.name,
        password: req.body.password
    };

    try {
        const checking = await LogInCollection.findOne({ name: req.body.name });

        if (checking) {
            if (checking.password === req.body.password) {
                return res.send("User details already exist");
            }
        } else {
            await LogInCollection.insertMany([data]);
            return res.status(201).render("about", { naming: req.body.name });
        }
    } catch (error) {
        console.error(error);
        return res.status(500).send("Internal Server Error");
    }

    // Ensure a default response in case of unexpected logic flow
    return res.status(400).send("Bad Request");
});

app.post('/login', async (req, res) => {
    try {
        const check = await LogInCollection.findOne({ name: req.body.name });

        if (check && check.password === req.body.password) {
            return res.status(201).render("about", { naming: `${req.body.password}+${req.body.name}` });
        } else {
            return res.send("Incorrect password");
        }
    } catch (e) {
        console.error(e);
        return res.status(500).send("Internal Server Error");
    }
});

app.listen(port, () => {
    console.log('Port connected');
});
