document.getElementById("askButton").addEventListener("click", async () => {
    const questionElem = document.getElementById("question");
    const answerDiv = document.getElementById("answer");
    const question = questionElem.value.trim();

    if (!question) {
        answerDiv.textContent = "請輸入問題！";
        return;
    }

    answerDiv.textContent = "正在思考中...";

    const formData = new FormData();
    formData.append("user_input", question);

    try {
        const response = await fetch("/get_response", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        
        if (data.error) {
            answerDiv.textContent = `錯誤：${data.error}`;
        } else {
            answerDiv.textContent = data.response;
        }
    } catch (error) {
        console.error(error);
        answerDiv.textContent = "發生錯誤，請稍後再試！";
    }
});