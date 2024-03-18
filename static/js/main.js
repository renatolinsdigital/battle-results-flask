const ENVIRONMENT_BASE_URL = 'http://localhost';
const ENVIRONMENT_PORT = 8080;

/* This Code is just for testing the API with some Javascript */

function renderEntries(entries) {
  entries.forEach(entry => {
    console.log('ID:', entry.id);
    console.log('Game Tag:', entry.gameTag);
    console.log('Player 1 Name:', entry.player1Name);
    console.log('Player 2 Name:', entry.player2Name);
    console.log('Winner Name:', entry.winnerName);
    console.log('Finished Date:', entry.finishedDate);
    console.log('--------------------------------');
  });
}

window.addEventListener('load', async () => {
  const entriesEndPoint = `${ENVIRONMENT_BASE_URL}:${ENVIRONMENT_PORT}/entries`;
  try {
    const response = await axios.get(entriesEndPoint);
    const entries = response.data.entries;
    renderEntries(entries);
  } catch (error) {
    console.error('Error fetching entries:', error);
  }
});

