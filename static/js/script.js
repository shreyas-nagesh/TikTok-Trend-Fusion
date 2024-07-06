document.addEventListener('DOMContentLoaded', function () {
    var input = document.querySelector('#search');
    var availableTags = JSON.parse(document.getElementById('trending-tags').textContent);

    $("#search").autocomplete({
        source: availableTags,
        minLength: 0, // Ensures the autocomplete shows all options on focus
        create: function () {
            $(this).data('ui-autocomplete')._renderItem = function (ul, item) {
                return $('<li>')
                    .append('<div><i class="fas fa-search autocomplete-icon"></i>' + item.label + '</div>')
                    .appendTo(ul);
            };
        }
    }).focus(function () {
        $(this).autocomplete("search", ""); // Triggers the autocomplete to show all options on focus
    });

    var tagify = new Tagify(input, {
        whitelist: availableTags,
        dropdown: {
            maxItems: 20,
            enabled: 0,
            closeOnSelect: false
        }
    });

    // Attach submit event listener to the form element
    var form = document.getElementById('searchForm');
    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            var loader = document.getElementById('video-loader');
            var audioLoader = document.getElementById('audio-loader');
            if (loader && audioLoader) {
                loader.style.display = 'block';
                audioLoader.style.display = 'block';
            }
            const formData = new FormData(this);
            fetch(this.action, {
                    method: 'POST',
                    body: formData
                }).then(response => response.text())
                .then(html => {
                    console.log("Response received for video generation");
                    loader.style.display = 'none';
                    document.getElementById('left-content').innerHTML = html;
                    // Trigger audio generation
                    fetch(generateAudioUrl, {
                            method: 'POST',
                            body: formData
                        }).then(response => response.json())
                        .then(data => {
                            console.log("Response received for audio generation");
                            audioLoader.style.display = 'none';
                            var audioContent = document.getElementById('audio-content');
                            var infoText = document.getElementById('info-text');
                            var promptText = document.getElementById('prompt-text');
                            var audioPlayer = document.getElementById('audio-player');
                            var audioSource = document.getElementById('audio-source');
                            if (data.audio_url) {
                                console.log("Audio URL: " + data.audio_url);
                                promptText.textContent = data.idea_description;
                                infoText.style.display = 'block';
                                audioSource.src = data.audio_url;
                                audioPlayer.style.display = 'block';
                            } else {
                                audioContent.innerHTML = '<p>No audio generated.</p>';
                            }
                            console.log("All done!");
                        });
                });
        });
    }
});