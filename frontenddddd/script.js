const plannerForm = document.getElementById('plannerForm');

plannerForm.addEventListener('submit', async (event) => {
  event.preventDefault(); // Prevent default form submission behavior

  const place = document.getElementById('place').value;
  const budget = document.getElementById('budget').value;
  const preferences = document.getElementById('preferences').value.toLowerCase().split(',').map(pref => pref.trim()); // Split and trim preferences
  const days = document.getElementById('days').value;

  const userData = {
    place: place,
    days: parseInt(days),
    budget: parseInt(budget),
    preferences: preferences,
  };

  try {
    const response = await fetch('http://127.0.0.1:5000/generate-itinerary', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    console.log("Itinerary Response:", data);

    // Handle itinerary data on the input page (consider user experience)
    // For example:
    // - Display a success message or visual indicator
    // - Optionally, provide a link or button to view the itinerary details on a separate page

  } catch (error) {
    console.error("Error fetching data:", error);
    // Handle errors by displaying an error message to the user
  }
});