function resolve_query() {
    user_query = document.getElementById("queryInput").value;
    fetch("/query-router", {
        method: "POST",
        headers: {
            "Content-Type": "application/json" 
        },
        body: JSON.stringify({
            'query': user_query
        })
    })
    .then(response => response.json())
    .then(data => {
        localStorage.setItem("user_query", JSON.stringify(user_query));
        localStorage.setItem("resolved_solution", JSON.stringify(data.resolved_solution))
        window.location.href = "/solution";
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

