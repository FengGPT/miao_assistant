const chatList = document.querySelector('.chat-list');

function getChatHistory() {
  fetch('http://localhost:5000/api/get_chat_history')
    .then(response => response.json())
    .then(chatRecords => {
      chatList.innerHTML = ''; // 清空之前的聊天记录

      // 对聊天记录数组进行倒序排序
      chatRecords.sort((a, b) => {
        const dateA = new Date(a.Date);
        const dateB = new Date(b.Date);
        return dateB - dateA;
      });

      chatRecords.forEach((record) => {
        const item = document.createElement('li');
        item.classList.add('chat-item');
        item.innerHTML = `
          <div class="time">${formatTime(record.Date)}</div>
          <div class="question">${record.Questions}</div>
          <div class="answer">${record.GPT_Answer}</div>
        `;
        chatList.appendChild(item);
      });
    })
    .catch(error => console.error(error));
}

// Add click event listener to the button
const getChatHistoryBtn = document.getElementById('getChatHistoryBtn');
getChatHistoryBtn.addEventListener('click', getChatHistory);


// Format the time in a readable format
function formatTime(dateTimeString) {
  const dateTime = new Date(dateTimeString);
  const options = { hour: 'numeric', minute: 'numeric' };
  return dateTime.toLocaleDateString('en-US') + ' ' + dateTime.toLocaleTimeString('en-US', options);
}
