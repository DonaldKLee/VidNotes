 // Runs again if the user's form does not submit. 
 // This makes it so that the video shows again
window.onload = function() {
    video_given();
    on_email();
};

function video_given() {
    link = document.getElementById('video_link').value
    video_player = document.getElementById('video_player')
    youtube_video_container = document.getElementById('youtube_video_container')

    // Remove https://www.youtube.com/watch?v=
    // Add https://www.youtube.com/embed/

    // Converts the shortened YouTube link to it's general link

    var new_link = link.replace('youtu.be/', 'youtube.com/watch?v=');

    var new_link = new_link.replace('watch?v=', 'embed/');

    // Converts the mobile YouTube link to it's general link
    var new_link = new_link.replace('m.youtube', 'youtube');

    // Removes the extra URL text if the video is from a playlist
    var new_link = new_link.split("&list=")[0];

    // Shows video preview
    video_player.src = new_link;

    // If it's a YouTube video, show the video
    if (new_link.includes("embed/")) {
        youtube_video_container.style.display = "block";
    }
    else { // Hides the video
        youtube_video_container.style.display = "none";
    }
}

function on_email() {
    email_text = document.getElementById("note_email").value;
    submit_button = document.getElementById("submit_button");
    if (email_text) {
        submit_button.value = "Generate link and Email me!"
    }
    else {
        submit_button.value = "Generate link!"
    }
}

function swap() {
    video = document.getElementById("youtube_video_container");
    form = document.getElementById("form");
    swap_button = document.getElementById("swap_button");
    
    document.getElementById("swap_icon").style.animation = "swap_spin 0.3s 1";

    if (swap_button.name  == "swap") { // Swap
        video.style.float = "left";
        video.style.right = "0%";
        video.style.left = "5%";

        form.style.left = "52.5%";
        swap_button.name = "Unswap";
    }
    else { // Unswap
        video.style.float = "right";
        video.style.left = "auto";
        video.style.right = "5%";

        form.style.left = "auto";
        swap_button.name = "swap";
    }

    setTimeout(() => { document.getElementById("swap_icon").style.animation = "none"; }, 300);

}