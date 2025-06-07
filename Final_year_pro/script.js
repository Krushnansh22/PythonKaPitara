// Mode Switcher Functionality
const modeToggle = document.getElementById('modeToggle');
const modeLabel = document.getElementById('modeLabel');

modeToggle.addEventListener('change', () => {
  if (modeToggle.checked) {
    document.body.classList.remove('dark-mode');
    document.body.classList.add('light-mode');
    modeLabel.textContent = 'Light Mode';
  } else {
    document.body.classList.remove('light-mode');
    document.body.classList.add('dark-mode');
    modeLabel.textContent = 'Dark Mode';
  }
});

// Initialize Default Mode
document.body.classList.add('dark-mode');

// Initialize Chart.js for Speedometer
const speedCtx = document.getElementById('speedometer').getContext('2d');

const speedData = {
  datasets: [{
    data: [0, 220],
    backgroundColor: ['#3498db', '#bdc3c7'],
    borderWidth: 0,
    circumference: 180,
    rotation: 270,
    cutout: '70%',
    hoverBackgroundColor: ['#2980b9', '#95a5a6']
  }]
};

const speedometer = new Chart(speedCtx, {
  type: 'doughnut',
  data: speedData,
  options: {
    responsive: true,
    animation: {
      animateRotate: true,
      duration: 1500
    },
    plugins: {
      tooltip: { enabled: false },
      legend: { display: false },
      // Custom plugin to display speed
      beforeDraw: function(chart) {
        const width = chart.width,
              height = chart.height,
              ctx = chart.ctx;
        ctx.save();
        ctx.font = 'bold ' + (height / 15) + 'px Arial';
        ctx.fillStyle = modeToggle.checked ? '#2c3e50' : '#ecf0f1';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        const speed = speedometer.data.datasets[0].data[0];
        ctx.fillText(`${speed} km/h`, width / 2, height / 1.8);
      }
    }
  }
});

// Initialize Chart.js for RPM Meter
const rpmCtx = document.getElementById('rpmMeter').getContext('2d');

const rpmData = {
  datasets: [{
    data: [0, 5],
    backgroundColor: ['#e74c3c', '#bdc3c7'],
    borderWidth: 0,
    circumference: 180,
    rotation: 270,
    cutout: '70%',
    hoverBackgroundColor: ['#c0392b', '#95a5a6']
  }]
};

const rpmMeter = new Chart(rpmCtx, {
  type: 'doughnut',
  data: rpmData,
  options: {
    responsive: true,
    animation: {
      animateRotate: true,
      duration: 1500
    },
    plugins: {
      tooltip: { enabled: false },
      legend: { display: false },
      // Custom plugin to display RPM
      beforeDraw: function(chart) {
        const width = chart.width,
              height = chart.height,
              ctx = chart.ctx;
        ctx.save();
        ctx.font = 'bold ' + (height / 15) + 'px Arial';
        ctx.fillStyle = modeToggle.checked ? '#2c3e50' : '#ecf0f1';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        const rpm = rpmMeter.data.datasets[0].data[0];
        ctx.fillText(`${rpm}k RPM`, width / 2, height / 1.8);
      }
    }
  }
});

// Function to update Speedometer
function updateSpeed(speed) {
  speedometer.data.datasets[0].data[0] = speed;
  speedometer.update();
}

// Function to update RPM Meter
function updateRPM(rpm) {
  rpmMeter.data.datasets[0].data[0] = rpm;
  rpmMeter.update();
}

// Simulate Real-time Data Updates
let currentSpeed = 0;
let currentRPM = 0;

setInterval(() => {
  // Simulate Speed Increase
  currentSpeed = (currentSpeed + Math.floor(Math.random() * 10)) % 240;
  updateSpeed(currentSpeed);
  // Simulate RPM based on Speed
  currentRPM = Math.min(5, Math.floor(currentSpeed / 40));
  updateRPM(currentRPM);
  // Optionally, you can add logic to trigger warning lights based on speed/RPM
}, 3000);

// Warning Light Activation Simulation
const warningLights = document.querySelectorAll('.warning-light');

warningLights.forEach(light => {
  setInterval(() => {
    const activate = Math.random() > 0.8; // 20% chance to activate
    if (activate) {
      light.classList.add('active');
      // Optionally, you can add more functionality like playing a sound or logging
      setTimeout(() => {
        light.classList.remove('active');
      }, 3000);
    }
  }, 7000);
});
