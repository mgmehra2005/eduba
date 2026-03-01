const problemStatement = document.getElementById("userProblemStatement");
const solutionContaier = document.getElementById("solutionCon");
const explainationContainer = document.getElementById("explainationCon");

window.addEventListener("load", function(){
    const user_query = JSON.parse(localStorage.getItem("user_query"));
    const resolved_solution = JSON.parse(localStorage.getItem("resolved_solution"));
    console.log(resolved_solution);   
    
    if (user_query !== null) {
        problemStatement.innerText = user_query;
    } else {
        problemStatement.innerText = "No problem statement found.";
    }

    if (resolved_solution !== null) {
        let solutionElement = this.document.createElement("p");
        solutionElement.id = "solutionText";
        
        if (typeof(resolved_solution["data"]) === "string") {
            solutionElement.innerText = JSON.parse(resolved_solution["data"])["final_answer"];
        } else {
            solutionElement.innerText = resolved_solution["data"]["final_answer"];
        }

        solutionElement.classList.add("solution-text");
        solutionContaier.appendChild(solutionElement);

        if (typeof(resolved_solution["data"]) === "string") {
            for (let explanation of JSON.parse(resolved_solution["data"])["stepwise_explanation"]) {
                let explainationElement = this.document.createElement("p");
                explainationElement.innerText = explanation;
                explainationElement.classList.add("explaination-text");
                explainationContainer.appendChild(explainationElement);
            }
        } else {
            for (let explanation of resolved_solution["data"]["stepwise_explanation"]) {
                let explainationElement = this.document.createElement("p");
                explainationElement.id = "explainationText";
                explainationElement.innerText = explanation;
                explainationElement.classList.add("explaination-text");
                explainationContainer.appendChild(explainationElement);
            }
        }

        if (typeof(resolved_solution["data"]) === "string") {
            data = JSON.parse(resolved_solution["data"])
        } else {
            data = resolved_solution["data"];
        }

        this.document.getElementById("concept_title").innerText = data["concept"];
        this.document.getElementById("difficulty-level").innerText = data["difficulty"];

    } else {
        solutionContaier.innerText = "No solution found.";
    }


    localStorage.removeItem("user_query");
    localStorage.removeItem("resolved_solution");
})
