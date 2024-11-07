document.addEventListener("alpine:init", () => {
  Alpine.data("FoodwasteApp", () => {
    return {
      Admin_Home_Page: true,
      add_new_questions: false,
      add_new_question_options: false,
      provide_question_answers: false,
      update_question_options: false,
      view_all_questions: false,
      add_new_admin_user_account: false,
      view_all_user_account: false,
      create_common_cause_game: false,
      create_environmental_anagram_game:false,
      game_instrcutions:false,
      prevention_Image_game: false,

      openHome(currentSection) {
        this.Admin_Home_Page = true;
        this.add_new_questions = false;
        this.add_new_question_options = false;
        this.provide_question_answers = false;
        this.update_question_options = false;
        this.view_all_questions = false;
        this.add_new_admin_user_account = false;
        this.view_all_user_account = false;
        this.create_common_cause_game = false;
        this.create_environmental_anagram_game=false;
        this.game_instrcutions=false;
        this.prevention_Image_game=false;

        if (currentSection == "add_new_questions") {
          this.Admin_Home_Page = false;
          this.add_new_questions = true;
        } else if (currentSection == "add_new_question_options") {
          this.Admin_Home_Page = false;
          this.add_new_question_options = true;
        } else if (currentSection == "provide_question_answers") {
          this.Admin_Home_Page = false;
          this.provide_question_answers = true;
        } else if (currentSection == "update_question_options") {
          this.Admin_Home_Page = false;
          this.update_question_options = true;
        } else if (currentSection == "view_all_questions") {
          this.Admin_Home_Page = false;
          this.view_all_questions = true;
        } else if (currentSection == "add_new_admin_user_account") {
          this.Admin_Home_Page = false;
          this.add_new_admin_user_account = true;
        } else if (currentSection == "view_all_user_account") {
          this.Admin_Home_Page = false;
          this.view_all_user_account = true;
        } else if (currentSection == "create_common_cause_game") {
          this.Admin_Home_Page = false;
          this.create_common_cause_game = true;
        }else if (currentSection == "create_environmental_anagram_game") {
          this.Admin_Home_Page = false;
          this.create_environmental_anagram_game = true;
        }else if (currentSection == "game_instrcutions") {
          this.Admin_Home_Page = false;
          this.game_instrcutions = true;
        }else if (currentSection == "prevention_Image_game") {
          this.Admin_Home_Page = false;
          this.prevention_Image_game = true;
        }
      },

      init() {
        this.startTimerWhyUs();
        //   this.activeImage = this.images.length > 0 ? this.images[0] : null;
      },
    };
  });
});




