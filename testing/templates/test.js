let video = document.getElementById("camera");
let captured = document.getElementById("captured");
let statusLight = document.getElementById("status-light");
let stream;

function startCamera() {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(s => {
      stream = s;
      video.srcObject = stream;
      setStatus(true);
    })
    .catch(err => {
      console.error(err);
      setStatus(false);
    });
}

function stopCamera() {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
    video.srcObject = null;
    setStatus(false);
  }
}

function captureImage() {
  let canvas = document.createElement("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0);
  captured.src = canvas.toDataURL("image/png");
}

function setStatus(success) {
  statusLight.className = "light " + (success ? "green" : "red");
}
