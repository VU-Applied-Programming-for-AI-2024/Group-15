// favorites.js

async function searchFavorites() {
    try {
      const email = document.getElementById('favoritesEmailInput').value.trim();
  
      if (!email) {
        alert('Please enter an email to search for favorites.');
        return;
      }
  
      const favorites = await getFavoritesByEmail(email);
  
      displayFavorites(favorites); // This function will be responsible for displaying favorites on the page
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to retrieve favorites. Please try again later.');
    }
  }
  
  async function getFavoritesByEmail(email) {
    const getFavesUrl = new URL('https://fitnessaicoach.azurewebsites.net/get_favorites');
    getFavesUrl.searchParams.append('email', email);
    try {
      const response = await fetch(getFavesUrl);
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const result = await response.json();
      if (result.status === 'success') {
        return result.favorites;
      } else {
        throw new Error(result.message);
      }
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
  }
  
  function displayFavorites(favorites) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ''; // Clear previous results

    if (favorites.length === 0) {
        resultsDiv.innerHTML = '<p>No favorites found for the given email.</p>';
        return;
    }

    const favoritesHTML = favorites.map((favorite) => {
        return `<div class="favorite-item">
                    <button class="favorite-button" data-email="${favorite.email}" data-schedule-name="${favorite.schedule_name}">
                        ${favorite.schedule_name}
                    </button>
                    <p>Email: ${favorite.email}</p>
                </div>`;
    });

    resultsDiv.innerHTML = favoritesHTML.join('');

    const favoriteButtons = resultsDiv.querySelectorAll('.favorite-button');
    favoriteButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const email = button.dataset.email;
            const scheduleName = button.dataset.scheduleName;
            loadSchedule(email, scheduleName);
        });
    });
}

function loadSchedule(email, scheduleName) {
    window.location.href = `schedule_display.html?email=${email}&schedule_name=${scheduleName}`;
  }