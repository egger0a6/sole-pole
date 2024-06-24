const btn = document.getElementById("linkBtn");

function copyLink() {
  const link = window.location.href;

  navigator.clipboard.writeText(link);
}