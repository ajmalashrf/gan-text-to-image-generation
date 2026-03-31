const promptForm = document.getElementById('prompt-form');
const promptInput = document.getElementById('prompt');
const generateBtn = document.getElementById('generate-btn');
const statusText = document.getElementById('status');
const resultImage = document.getElementById('result-image');

async function handleSubmit(event) {
  event.preventDefault();

  const prompt = promptInput.value.trim();
  if (prompt.length < 3) {
    statusText.textContent = 'Please enter at least 3 characters.';
    return;
  }

  generateBtn.disabled = true;
  statusText.textContent = 'Generating image...';

  try {
    const response = await fetch('/api/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Generation failed');
    }

    resultImage.src = `${data.imageUrl}?t=${Date.now()}`;
    resultImage.hidden = false;
    statusText.textContent = `Done! Prompt: "${data.prompt}"`;
  } catch (error) {
    statusText.textContent = `Error: ${error.message}`;
  } finally {
    generateBtn.disabled = false;
  }
}

promptForm.addEventListener('submit', handleSubmit);
