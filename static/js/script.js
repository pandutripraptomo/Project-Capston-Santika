// static/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    // Fungsi untuk menambahkan pesan ke chatbox
    function appendMessage(text, className) { // className sekarang bisa berupa string tunggal atau string dengan spasi
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message'); // Tambahkan kelas 'message' terlebih dahulu

        // Tambahkan kelas-kelas lain dari argumen className
        // Jika className mengandung spasi (misal: 'bot-message typing-indicator'),
        // kita perlu memisahkannya dan menambahkannya satu per satu.
        if (className) {
            className.split(' ').forEach(cls => {
                if (cls) { // Pastikan bukan string kosong dari split
                    messageDiv.classList.add(cls);
                }
            });
        }
        
        messageDiv.textContent = text;
        chatBox.appendChild(messageDiv);
        // Scroll ke bawah secara otomatis
        chatBox.scrollTop = chatBox.scrollHeight;
        return messageDiv; // Mengembalikan elemen yang dibuat untuk manipulasi lebih lanjut (misal: menghapus)
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Mencegah form dari reload halaman
        const message = userInput.value.trim();

        if (message) {
            // Tampilkan pesan pengguna di chatbox
            appendMessage(message, 'user-message');
            userInput.value = ''; // Kosongkan input setelah mengirim

            // Tampilkan indikator "Typing..."
            const typingIndicator = appendMessage('Typing...', 'bot-message typing-indicator');

            try {
                // Kirim pesan ke backend Flask
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                });

                if (!response.ok) {
                    // Tangani jika respons HTTP tidak berhasil (misal: 400, 500)
                    const errorData = await response.json();
                    throw new Error(`HTTP error! Status: ${response.status}. Detail: ${errorData.error || 'Unknown error'}`);
                }

                const data = await response.json();
                
                // Hapus indikator "Typing..."
                typingIndicator.remove();
                // Tampilkan respons dari chatbot
                appendMessage(data.response, 'bot-message');

            } catch (error) {
                console.error('Error:', error);
                // Hapus indikator "Typing..."
                typingIndicator.remove();
                // Tampilkan pesan error kepada pengguna
                appendMessage('Oops! Failed to get response from AI. Please check your internet connection or try again later.', 'bot-message error-message');
            } finally {
                // Pastikan chatbox selalu discroll ke bawah setelah ada pesan baru
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        }
    });
});