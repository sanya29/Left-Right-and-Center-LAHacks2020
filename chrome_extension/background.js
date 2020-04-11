chrome.identity.getProfileUserInfo(function(info) {

  chrome.tabs.onUpdated.addListener(
      function(tabId, changeInfo, tab) {
        
        if (changeInfo.url) {
          
          var classInfo = ''

          if (changeInfo.url.indexOf('bbc.com') !== -1) {    // h1
            classInfo = 'story-body__h1'
          } else if (changeInfo.url.indexOf('bloomberg.com') !== -1) {     // h1
            classInfo = 'lede-text-v2__hed'
          } else if (changeInfo.url.indexOf('buzzfeednews.com') !== -1) {    // h1
            classInfo = 'news-article-header__title'
          } else if (changeInfo.url.indexOf('cnn.com') !== -1) {     // h1
            classInfo = 'pg-headline'
          } else if (changeInfo.url.indexOf('foxnews.com') !== -1) {     // h1
            classInfo = 'headline'
          } else if (changeInfo.url.indexOf('motherjones.com') !== -1) {     // h1
            classInfo = 'entry-title'
          } else if (changeInfo.url.indexOf('thewashingtontimes.com') !== -1) {    // h1
            classInfo = 'page-headline'
          } else if (changeInfo.url.indexOf('vox.com') !== -1) {   // h1
            classInfo = 'c-page-title'
          }
        console.log('email: ' + info.email)
          var data_to_send_1 = {'url': changeInfo.url, 'classInfo': classInfo}
          var tags = ''
          var api_url_1 = 'https://us-central1-la-hacks-272508.cloudfunctions.net/update-database-p1';
          var api_url_2 = 'https://us-central1-la-hacks-272508.cloudfunctions.net/update-database-p2';
          
          fetch(api_url_1, {
            method: 'POST',
            body: JSON.stringify(data_to_send_1),
            headers:{
              'Content-Type': 'application/json'
            } })
          .then(data => { data.text().then(function(value) {
              tags = value
              
              var data_to_send_2 = {'url': changeInfo.url, 'tags': tags, 'id':info.email}

              fetch(api_url_2, {
                method: 'POST',
                body: JSON.stringify(data_to_send_2),
                headers:{
                  'Content-Type': 'application/json'
                } })
              .then(data => { data.text().then(function(value) {
                  console.log('Success!')
                })
              })
              .catch(error => console.error('Error:', error));

            }) 
          })
          .catch(error => console.error('Error:', error));
        }
      }
    );
    
});
