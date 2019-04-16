//
//  Firestore Cloud Function to Update Matchmaking
//  Will Update Matchmaking Results for Everyone
//  If Any User Fully Completes their Onboarding
// 

const functions = require('firebase-functions');

function triggerDocumentAnyChange() {
    // [START trigger_document_any_change]
    exports.updateUser = functions.firestore
    .document('users/{userId}')
    .onUpdate((change, context) => {

      // Retrieve the current and previous value
      const data = change.after.data();
      const previousData = change.before.data();

      // We'll only update if the name has changed.
      // This is crucial to prevent infinite loops.
      if (data.name == previousData.name) return null;

      // If the User hasn't fully completed their registration,
      // we won't update the recommender results
      if (!('selected_strategies_keywords' in data) || !('selected_skills_keywords' in data)) {
          return null;
      }
      // Otherwise, re-run matchmaking on every user 
      // by calling Selasi's function

    });
    // [END trigger_document_any_change]
  }