# Left, Right and Center (LA-Hacks 2020)

## Description

In today's polarized societies, the integral job of the news media as an unbiased and fair reciprocator of the facts has changed dramatically. We tend to want to hear the news we that sounds good to us, and this restricts us to a narrow point-of-view that very often introduces bias into our thinking. Left, Right and Center attempts to braoden our ideas by encouraging us to incorporate news from various sources, removing us from our bubbles and allowing us to see certain issues from a different point-of-view. This Chrome extension keeps tracks of the articles a user reads from a particular news organization, identifies the topics that is most relevant to them and suggests articles of the same topics but from a different, more polar news media source.

Check out our DevPost writeup for more information: https://devpost.com/software/left-right-and-center

## Setup

### Installation of the Chrome extension.

Download the files above first.

1. Ensure that you are logged into your Google account on the Chrome browser.
2. In the search bar, type in:
```bash
chrome://extensions
```
3. In the top left corner, click on the 'Load unpacked' button.
4. Select the 'chrome_extension' folder downloaded.

## How it works

The front-end of this project uses JavaScript and HTML while the back-end is handled with Python. The backend exists in the cloud which was deployed using Google Cloud Platform's Cloud Function services and also consists of a Google Cloud Firestore database to store information about the topics and news organizations the user cares about the most.

When a user clicks on a particular article, the URL for this article is sent to a deployed Python function that first scrapes the website of the URL for the title of the article, finding the relevant topics in the article and adding it to a 'tags' collection in the Firestore database. The relevant topics are selected using NLP, which is done with the spaCY Python package. The database is also updated to keep track of the number of times a user visits a particular news organization's website. When the user clicks on the extension, a popup appears with the topics the user cares about the most, their apparent political leaning based on where they get their news from, and three articles from an opposing viewpoint.

## Team members

* *Adithya Nair (GitHub: **@git-adithyanair**)*
* *Aritra Mullick (GitHub: **@aritramullick**)*
* *Abhishek Marda (GitHub: **@AbhishekMarda**)*
* *Sanya Srivastava (GitHub: **@sanya29**)*

