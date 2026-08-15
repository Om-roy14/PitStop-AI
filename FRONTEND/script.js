// ==========================================
// GET ELEMENTS
// ==========================================

const loginCard =
    document.getElementById("loginCard");

const registerCard =
    document.getElementById("registerCard");

const userCard =
    document.getElementById("userCard");


// ==========================================
// SHOW LOGIN
// ==========================================

function showLogin() {

    loginCard.classList.remove("hidden");

    registerCard.classList.add("hidden");

    userCard.classList.add("hidden");
}


// ==========================================
// SHOW REGISTER
// ==========================================

function showRegister() {

    loginCard.classList.add("hidden");

    registerCard.classList.remove("hidden");

    userCard.classList.add("hidden");
}


// ==========================================
// SHOW USER
// ==========================================

function showUser(user) {

    loginCard.classList.add("hidden");

    registerCard.classList.add("hidden");

    userCard.classList.remove("hidden");


    document.getElementById("userName")
        .textContent = user.name;


    document.getElementById("userEmail")
        .textContent = user.email;
}


// ==========================================
// REGISTER
// ==========================================

document
    .getElementById("registerForm")
    .addEventListener("submit", async function (event) {

        event.preventDefault();


        const name =
            document
                .getElementById("registerName")
                .value
                .trim();


        const email =
            document
                .getElementById("registerEmail")
                .value
                .trim();


        const password =
            document
                .getElementById("registerPassword")
                .value;
        const linkedin_id =
            document
                .getElementById("registerLinkedin")
                .value;
        const github_id =
            document
                .getElementById("registerGithub")
                .value;


        const message =
            document
                .getElementById("registerMessage");


        try {

            const response = await fetch(
                "/register",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        name: name,

                        email: email,

                        password: password,

                        linkedin_id : linkedin_id,

                        github_id : github_id,

                    })

                }
            );


            const data =
                await response.json();


            if (!response.ok) {

                message.classList.remove("success");

                message.textContent =
                    data.detail;

                return;
            }


            message.classList.add("success");

            message.textContent =
                "Account created successfully.";


            document
                .getElementById("registerForm")
                .reset();


            setTimeout(
                showLogin,
                1000
            );


        } catch (error) {

            message.textContent =
                "Unable to connect to server.";

        }

    });


// ==========================================
// LOGIN
// ==========================================

document
    .getElementById("loginForm")
    .addEventListener("submit", async function (event) {

        event.preventDefault();


        const email =
            document
                .getElementById("loginEmail")
                .value
                .trim();


        const password =
            document
                .getElementById("loginPassword")
                .value;


        const message =
            document
                .getElementById("loginMessage");


        try {

            const response = await fetch(
                "/login",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        email: email,

                        password: password

                    })

                }
            );


            const data =
                await response.json();


            if (!response.ok) {

                message.textContent =
                    data.detail;

                return;
            }


            // Store logged-in user

            localStorage.setItem(
                "user",
                JSON.stringify(data.user)
            );


            // Display user

            showUser(
                data.user
            );


        } catch (error) {

            message.textContent =
                "Unable to connect to server.";

        }

    });


// ==========================================
// LOGOUT
// ==========================================

function logout() {

    localStorage.removeItem("user");

    document
        .getElementById("loginForm")
        .reset();

    showLogin();
}


// ==========================================
// CHECK LOGIN WHEN PAGE LOADS
// ==========================================

window.addEventListener(
    "load",
    function () {

        const storedUser =
            localStorage.getItem("user");


        if (storedUser) {

            const user =
                JSON.parse(storedUser);

            showUser(user);

        } else {

            showLogin();

        }

    }
);