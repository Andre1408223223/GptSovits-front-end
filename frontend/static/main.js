// ✅ Only one toggleSettings click handler
document.getElementById("toggleSettings").addEventListener("click", () => {
  const settings = document.getElementById("extraSettings");
  const isVisible = settings.style.display === "block";
  settings.style.display = isVisible ? "none" : "block";
});

function loading_animation(mode) {
  let loading = document.querySelector(".loading-animation");

  if (!loading) {
    loading = document.createElement("div");
    loading.className = "loading-animation";
    loading.textContent = "Synthesizing audio...";
    loading.style.fontStyle = "italic";
    loading.style.marginTop = "10px";
    loading.style.color = "#555";
    const form = document.getElementById("synthForm");
    form.appendChild(loading);
  }

  if (mode) {
    loading.style.display = "block";
  } else {
    loading.style.display = "none";
  }
}

function prepare_data() {
  // Helper to safely get element by id and return null if not found
  const getEl = (id) => document.getElementById(id);

  // Helper to parse int safely, fallback to default if invalid
  const parseIntSafe = (value, def = 0) => {
    const parsed = parseInt(value);
    return isNaN(parsed) ? def : parsed;
  };

  // Helper to parse float safely, fallback to default if invalid
  const parseFloatSafe = (value, def = 0) => {
    const parsed = parseFloat(value);
    return isNaN(parsed) ? def : parsed;
  };

  const data = {
    model: getEl("model")?.value || "",
    infer_text: getEl("text")?.value || "",

    text_split_method: getEl("text_split_method")?.value || "",
    batch_size: parseIntSafe(getEl("batch_size")?.value, 1),
    batch_threshold: parseFloatSafe(getEl("batch_threshold")?.value, 0),

    split_bucket: getEl("split_bucket")?.checked || false,

    speed_factor: parseFloatSafe(getEl("speed_factor")?.value, 1),
    streaming_mode: getEl("streaming_mode")?.checked || false,
    seed: parseIntSafe(getEl("seed")?.value, 0),
    parallel_infer: getEl("parallel_infer")?.checked || false,

    repetition_penalty: parseFloatSafe(getEl("repetition_penalty")?.value, 1),
    top_k: parseIntSafe(getEl("top_k")?.value, 0),
    top_p: parseFloatSafe(getEl("top_p")?.value, 1),
    temperature: parseFloatSafe(getEl("temperature")?.value, 1),

    sample_steps: parseIntSafe(getEl("sample_steps")?.value, 1),
    super_sampling: getEl("super_sampling")?.checked || false,

    output_file: getEl("output_file")?.value || "",
  };

  return data;
}

async function generate_tts() {
  loading_animation(true);

  const data = prepare_data();

  try {
    const response = await fetch("/synthesise", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.statusText}`);
    }

    // Get binary audio data as a Blob
    const audioBlob = await response.blob();
    const audioUrl = URL.createObjectURL(audioBlob);

    // Clear previous buttons or audio
    const container = document.getElementById("audioContainer");
    container.innerHTML = "";

    // Create the play button
    const playButton = document.createElement("button");
    playButton.className = "synth-play-button";
    playButton.textContent = "Play Audio";

    // Create audio element but keep it hidden (or you can skip adding it to DOM)
    const audio = new Audio(audioUrl);

    // When button is clicked, play the audio
    playButton.addEventListener("click", () => {
      audio.play();
    });

    // Append the play button to the container
    container.appendChild(playButton);

    // Optionally, clean up the URL after audio ends
    audio.onended = () => {
      URL.revokeObjectURL(audioUrl);
    };
  } catch (error) {
    console.error("Error generating TTS:", error);
    alert("Failed to generate TTS: " + error.message);
  } finally {
    loading_animation(false);
  }
}

document.getElementById("synthForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  generate_tts();
});
