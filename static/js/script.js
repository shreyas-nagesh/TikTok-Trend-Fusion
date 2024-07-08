document.addEventListener('DOMContentLoaded', function () {
    var input = document.querySelector('#main-search');
    var availableTags = JSON.parse(document.getElementById('trending-tags').textContent);

    $("#main-search").autocomplete({
        source: availableTags,
        minLength: 0, // Ensures the autocomplete shows all options on focus
        create: function () {
            $(this).data('ui-autocomplete')._renderItem = function (ul, item) {
                return $('<li>')
                    .append('<div><i class="fas fa-search"></i>' + item.label + '</div>')
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
            if (loader) {
                document.getElementById("trend-message").style.display = 'none';
                loader.style.display = 'block';
                audioLoader.style.display = 'none';
            }
            const formData = new FormData(this);
            fetch(this.action, {
                    method: 'POST',
                    body: formData
                }).then(response => response.text())
                .then(html => {
                    console.log("Response received for video generation");
                    loader.style.display = 'none';
                    audioLoader.style.display = 'block';
                    document.getElementById('left-content').style.display = 'block';
                    document.getElementById('right-content').style.display = 'block';
                    document.getElementById('body-content').innerHTML = html;
                    fetch('/generate_idea', {
                            method: 'POST',
                            body: formData
                        }).then(response => response.json())
                        .then(data => {
                            console.log("Response received for idea and concept");
                            var ideaContent = document.getElementById('idea-content');
                            ideaContent.style.display = 'block';
                            document.getElementById('audio-loader').style.display = 'none';
                            document.getElementById('audio-loader-2').style.display = 'block';
                            var ideaText = document.getElementById('idea-text');
                            var conceptText = document.getElementById('concept-text');
                            var infoText = document.getElementById('info-text');

                            ideaText.textContent = data.idea;
                            conceptText.textContent = data.concept;
                            infoText.style.display = 'block';
                            return fetch('/generate_media', {
                                method: 'POST',
                                body: formData
                            });
                        })
                        .then(response => response.json())
                        .then(data => {
                            console.log("Response received for audio generation");
                            document.getElementById('audio-loader-2').style.display = 'none';
                            var audioContent = document.getElementById('audio-content');
                            audioContent.style.display = 'block';
                            var audioSource = document.getElementById('audio-source');
                            var audioPlayer = document.getElementById('audio-player');

                            if (data.audio_url) {
                                audioSource.src = data.audio_url;
                                audioPlayer.style.display = 'block';
                                var audioElement = document.getElementById('audio-element');
                                audioElement.load();
                                audioElement.play();
                            } else {
                                audioContent.innerHTML = '<p>No audio generated.</p>';
                            }
                            var imageElement = document.getElementById('generated-image');
                            imageElement.src = data.img_url;
                            imageElement.style.display = 'block';

                            console.log("All done!");
                        });
                });
        });
    }
});