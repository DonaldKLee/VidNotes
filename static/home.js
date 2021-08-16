function video_given() {
    link = document.getElementById('video_link').value
    video_player = document.getElementById('video_player')

    // Remove https://www.youtube.com/watch?v=
    // Add https://www.youtube.com/embed/
    var new_link = link.replace('watch?v=', 'embed/');

    // Shows video preview
    video_player.src = new_link;


    // If it's a YouTube video, show the video
    if (new_link.includes("embed/")) {
        video_player.style.display = "block";
    }
    else { // Hides the video
        video_player.style.display = "none";
    }
}