// ✅ Only one toggleSettings click handler
document.getElementById("toggleSettings").addEventListener("click", () => {
  const settings = document.getElementById("extraSettings");
  const isVisible = settings.style.display === "block";
  settings.style.display = isVisible ? "none" : "block";
});

// ✅ Form submit handler
document.getElementById("synthForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    model: document.getElementById("model").value,
    infrance_text: document.getElementById("inference_text").value,
    output_language: document.getElementById("output_language").value,
    cut_punc: document.getElementById("punctuation").checked
      ? [",", ".", ";", "?", "!", "、", "，", "。", "？", "！", "；", "：", "…"]
      : null,

    top_k: parseFloat(document.getElementById("top_k").value),
    top_p: parseFloat(document.getElementById("top_p").value),
    temperature: parseFloat(document.getElementById("temperature").value),
    speed: parseFloat(document.getElementById("speed_setting").value),
    sample_steps: parseInt(document.getElementById("sample_steps").value),
    if_sr: document.getElementById("if_sr").checked,
    output_file: document.getElementById("output_file").value,
  };

  try {
    const response = await fetch("/synthesise", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Server error:", errorText);
      alert("Server error: " + errorText);
      return;
    }

    const blob = await response.blob();
    const audioUrl = URL.createObjectURL(blob);

    // Create Play button
    const playButton = document.createElement("button");
    playButton.textContent = "▶ Play Synthesized Audio";
    playButton.className = "synth-play-button";

    // Prevent form submission if clicked
    playButton.type = "button";

    // Insert the button after the form's submit button
    const form = document.getElementById("synthForm");
    const submitButton = form.querySelector('input[type="submit"]');
    submitButton.insertAdjacentElement("afterend", playButton);

    // Create and control audio playback
    const audio = new Audio(audioUrl);
    playButton.addEventListener("click", () => {
      audio.play();
    });
  } catch (err) {
    console.error("Request failed:", err);
    alert("Error sending data.");
  }
});
