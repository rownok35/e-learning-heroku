const url = window.location.href
console.log("hello!")
    // console.log(url)
    // console.log(`${url}/save/`)

const quizForm = document.getElementById("quiz-form");
const csrf = document.getElementsByName("csrfmiddlewaretoken");
const scorebox = document.getElementById("score-box");
const resultbox = document.getElementById("result-box");


const sendData = (e) => {
    e.preventDefault();
    const element = [...document.getElementsByClassName("ans")]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    element.forEach(el => {
        if (el.checked) {
            data[el.name] = el.value
        } else {
            if (!data[el.name]) {
                data[el.name] = null
            }
        }
    })

    $.ajax({
        type: 'POST',
        url: `${url}/save/`,
        data: data,
        success: function(response) {
            // console.log(response)
            const results = response.Results;
            const Score = response.Score;
            const Score2 = response.Score2;
            const Percentage_Score = response.Percentage_Score;
            scorebox.innerHTML = `${response.passed ? 'Congratulations!': 'Ups..:('} Your score is ${Score}`


            // console.log("Results: ", results);
            // console.log("Scores: ", Score);
            // console.log("Scores2: ", Score2);
            // console.log("Percentage_Score: ", Percentage_Score);
            quizForm.style.display = "none";
            results.forEach(res => {
                const resdiv = document.createElement("div");
                resdiv.innerHTML += res;
                const cls = ['p-3', 'h6', 'container', 'mt-4'];
                resdiv.classList.add(...cls);
                if (res.includes("wrong") || res.includes("no")) {
                    resdiv.classList.add('bg-danger')
                } else {
                    resdiv.classList.add('bg-success')
                }
                // const body = document.getElementsByTagName('BODY')[0];
                resultbox.append(resdiv);

                console.log(res)
            })
        },
        error: function(error) {
            console.log(error)
        }
    })



}

quizForm.addEventListener('submit', e => {
    e.preventDefault();
    sendData(e);
})