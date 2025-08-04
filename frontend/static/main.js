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
  const data = {
    model: document.getElementById("model").value,
    infer_text: document.getElementById("text").value,

    text_split_method: document.getElementById("text_split_method").value,
    batch_size: parseInt(document.getElementById("batch_size").value),
    batch_threshold: parseFloat(
      document.getElementById("batch_threshold").value
    ),
    split_bucket: document.getElementById("split_bucket").checked,

    speed_factor: parseFloat(document.getElementById("speed_factor").value),
    streaming_mode: document.getElementById("streaming_mode").checked,
    seed: parseInt(document.getElementById("seed").value),
    parallel_infer: document.getElementById("parallel_infer").checked,

    repetition_penalty: parseFloat(
      document.getElementById("repetition_penalty").value
    ),
    top_k: parseInt(document.getElementById("top_k").value),
    top_p: parseFloat(document.getElementById("top_p").value),
    temperature: parseFloat(document.getElementById("temperature").value),

    sample_steps: parseInt(document.getElementById("sample_steps").value),
    super_sampling: document.getElementById("super_sampling").checked,

    output_file: document.getElementById("output_file").value,
  };

  return data;
}

function generate_tts() {
  // Create or show loading animation
  loading_animation(true);

  data = prepare_data();

  if (document.getElementById("streaming_mode").checked) {
    console.log("Streaming mode is enabled.");
  } else {
    console.log("Streaming mode is disabled.");
  }

  loading_animation(false);
}

document.getElementById("synthForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  generate_tts();
});
