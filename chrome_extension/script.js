chrome.identity.getProfileUserInfo(function(info) {

	var api_url_3 = 'https://us-central1-la-hacks-272508.cloudfunctions.net/retrieve-from-database'
	var data_to_send = {'id': info.email}

    setTimeout(() => {
	fetch(api_url_3, {
		method: 'POST',
		body: JSON.stringify(data_to_send),
		headers:{
		  'Content-Type': 'application/json'
		} })
	.then(data => { data.text().then(function(value) {

			if (value == 'not_enough_tags') {
				var array = value.split('~')

				document.getElementById("history-para").innerHTML = "You haven't read enough articles for us to get a good understanding of what suggestions we need to give you!";
				document.getElementById("general-para").innerHTML = "Explore the internet, and we'll be here with other things for you to read!"
				
			} else {

				var array = value.split('~')

				document.getElementById("history-para").innerHTML = "You've been seeing a lot of news about " + array[5] + " and " + array[6] + ", primarily from " + array[3] + ". Your political views seem to be " + array[4] + ", so consider checking out the articles below.";
				document.getElementById("general-para").innerHTML = "A discussion meets its purpose when both sides of the story are heard."
				document.getElementById("suggestion-para").innerHTML = "Here is a list of suggested websites you could try out that would give you an alternate view."

				document.getElementById("suggested-website-1").innerHTML = array[0];
				document.getElementById("suggested-website-para-1").href = array[0];
			
				document.getElementById("suggested-website-2").innerHTML = array[1];
				document.getElementById("suggested-website-para-2").href = array[1];

				document.getElementById("suggested-website-3").innerHTML = array[2];
				document.getElementById("suggested-website-para-3").href = array[2];

			}

		}) 
	})
	.catch(error => console.error('Error:', error));
    }, 5000);

});
