document.getElementById("plannerForm").addEventListener("submit", async function(event) {
  event.preventDefault(); // Prevent the form from submitting normally

  // Show loading spinner while fetching data
  document.getElementById("loading").style.display = "block";
  document.getElementById("results").innerHTML = ""; // Clear previous results

  // Collect form data
  const place = document.getElementById("place").value;
  const budget = parseFloat(document.getElementById("budget").value);
  const preferences = document.getElementById("preferences").value;

  // Prepare the data to send to the backend
  const requestData = {
      place: place,
      budget: budget,
      preferences: preferences,
  };

  try {
      // Make the POST request to the backend
      const response = await fetch("http://localhost:3000/plan-trip", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify(requestData),
      });

      const data = await response.json();

      // Hide loading spinner
      document.getElementById("loading").style.display = "none";

      // Check if the response contains recommendations
      if (data.recommendations && data.recommendations.length > 0) {
          displayResults(data.recommendations);
      } else {
          document.getElementById("results").innerHTML = "No destinations found within your budget and preferences.";
      }
  } catch (error) {
      // Hide loading spinner and show error message if there's an issue
      document.getElementById("loading").style.display = "none";
      document.getElementById("results").innerHTML = "An error occurred. Please try again.";
      console.error("Error:", error);
  }
});

// Function to display results on the page
function displayResults(recommendations) {
  const resultsContainer = document.getElementById("results");
  resultsContainer.innerHTML = ""; // Clear previous results

  recommendations.forEach((place, index) => {
      const placeElement = document.createElement("div");
      placeElement.classList.add("place");

      placeElement.innerHTML = `
          <h3>${index + 1}. ${place.name}</h3>
          <p><strong>Address:</strong> ${place.address}</p>
          <p><strong>Rating:</strong> ${place.rating}</p>
          <p><strong>Estimated Cost:</strong> ₹${place.estimated_cost}</p>
      `;
      resultsContainer.appendChild(placeElement);
  });
}
