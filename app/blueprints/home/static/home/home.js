const fileUpload = document.getElementById('uploadForm');
fileUpload.addEventListener('change', uploadImage);

/*document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        alert('Data uploaded successfully!');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error uploading data!');
    });
});*/

function uploadImage(event)
{
    var url = new URL(window.location.href).origin + "/upload";
    const files = event.target.files
    var requestBody = new FormData();
    requestBody.append('file', files[0]);
        
    fetch(url, {
        method: 'POST',
        body: requestBody
    })
    .then(function(response) {
        return response.text();
    })
    .then(function(data) {
        data = JSON.parse(data);
        succeed = data.succeed;
        result = data.message;
        if (succeed == false){
            showError(result)
        }
        else
        {
            displayImg.src = data
            displayImg.style.display = 'block';
            clearErrors(message);
        }
    })
    .catch(function(error) {
        console.error('Fetch error:', error);
    });

    event.preventDefault();
}

