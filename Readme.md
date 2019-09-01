# Give Me Feedback

## Status: WIP

## Main Idea

The "owner" creates a "board" on which he can list a bunch of "topics".
Everyone can now for each topic
- mark as "interesting/boring"
- mark as "took too much time/was too fast"
- add comment(s)
- see what everyone else thought


# Log

- Created project give-me-feedback.firebaseapp.com
- `database` is https://github.com/firebase/quickstart-js/blob/master/database/README.md -- rest happens in there
- `firebase login`
- `firebase use  --add`, alias is test
- `firebase serve` to start a local test -- which could not be tested because Google login does not work locally
- `firebase deploy` to deploy to web version, now login works, but the test itself does not
- In console, enable databse (everyone may read/write) -- saving messages works.  Check out database
  [contents](https://console.firebase.google.com/project/give-me-feedback/database/give-me-feedback/data).
