// Get recommendations from localStorage
const recommendations = JSON.parse(localStorage.getItem('recommendations'));

// Get the journey map container
const journeyMap = document.getElementById('journey-map');

// Check if recommendations exist
if (recommendations && recommendations.length > 0) {
  recommendations.forEach((rec, index) => {
    // Create a step container
    const step = document.createElement('div');
    step.className = 'journey-step';

    // Add an icon for the step
    const icon = document.createElement('div');
    icon.className = 'icon';
    icon.textContent = index + 1; // Step number
    step.appendChild(icon);

    // Add information for the step
    const info = document.createElement('div');
    info.className = 'info';
    info.innerHTML = `
      <h3>${rec.name}</h3>
      <p><strong>Address:</strong> ${rec.address}</p>
      <p><strong>Rating:</strong> ${rec.rating || "N/A"}</p>
      <p><strong>Estimated Cost:</strong> ₹${rec.estimated_cost || "N/A"}</p>
    `;
    step.appendChild(info);

    // Append the step to the journey map
    journeyMap.appendChild(step);

    // Add an arrow to connect steps, except after the last step
    if (index < recommendations.length - 1) {
      const arrow = document.createElement('div');
      arrow.className = 'journey-arrow';
      journeyMap.appendChild(arrow);
    }
  });
} else {
  journeyMap.innerHTML = '<p>No recommendations found. Please try planning your trip again.</p>';
}
