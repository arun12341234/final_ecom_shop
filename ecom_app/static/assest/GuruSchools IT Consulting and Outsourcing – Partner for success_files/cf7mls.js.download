(function ($) {
  //jQuery time
  var current_fs, next_fs, previous_fs; //fieldsets
  var left, opacity, scale; //fieldset properties which we will animate
  var animating; //flag to prevent quick multi-click glitches
  var has_response = false;
  var preview_clicked = false;

  jQuery(document).ready(function ($) {

    // Transition effects
    $("form.wpcf7-form").each(function (index, el) {
      cf7mls_transition_effects(el, 'effects_in');
    });

    $("form.wpcf7-form").each(function (index, el) {
      var totalFieldset = 0;
      var this_form = $(el);
      var findFieldset = $(el).find("fieldset.fieldset-cf7mls");
      if (findFieldset.length > 0) {
        this_form.addClass('cf7mls')
        $.each(findFieldset, function (i2, el2) {
          if (i2 == 0) {
            $(el2).addClass("cf7mls_current_fs");
          }

          jQuery(el2).attr("data-cf7mls-order", i2);
          totalFieldset = totalFieldset + 1;
          //disable next button if the fieldset has  wpcf7-acceptance
          var acceptances = jQuery(el2).find("input:checkbox.wpcf7-acceptance");
          if (acceptances.length) {
            cf7mls_toggle_next_btn(acceptances, el2);
          }
        });
        $.each(findFieldset, function (i2, el2) {
          if (i2 == totalFieldset - 1) {
            $(el2)
              .find(".cf7mls_next")
              .remove();
          }
        });
        $(el).attr("data-count-fieldset", totalFieldset);
        //on form submit
        if (cf7mls_object.disable_enter_key) {
          $(el)
            .find('[type="submit"]')
            .click(function (event) {
              var findFieldset = $(el).find(
                "fieldset.fieldset-cf7mls.cf7mls_current_fs"
              );
              if (findFieldset.data("cf7mls-order") != totalFieldset - 1) {
                findFieldset.find(".cf7mls_next").click();
                return false;
              }
            });
        } else {
          $(el).submit(function (event) {
            var findFieldset = $(el).find(
              "fieldset.fieldset-cf7mls.cf7mls_current_fs"
            );
            if (findFieldset.data("cf7mls-order") != totalFieldset - 1) {
              findFieldset.find(".cf7mls_next").click();
              return false;
            }
          });
        }
      }
      //answer fields
      $(el)
        .find("input.wpcf7-cf7_answer")
        .each(function (njt_a_i, njt_a_e) {
          var $this = $(njt_a_e);
          var qf = this_form.find('[name="' + $this.data("qf") + '"]');
          var sp = $("span.wpcf7-cf7_answer_" + $this.data("qf"));
          var arrChecked = [];
          var isCheckbox =
            $this.data("qf").indexOf("cbmls") >= 0 ? true : false;

          if (isCheckbox) {
            qf = this_form.find('[name="' + $this.data("qf") + "[]" + '"]');
            qf.on("change", function (event) {
              event.preventDefault();
              var _val = $(this).val();
              var arrCheckedIndex = $.inArray(_val, arrChecked);
              if (this.checked) {
                if (arrCheckedIndex === -1) arrChecked.push(_val);
              } else {
                arrChecked.splice(arrCheckedIndex, 1);
              }
              sp.text(arrChecked.toString());
              $this.val(arrChecked.toString());
            });
          } else {
            if (qf.val()) {
              var _val = qf.val();
              sp.text(_val);
              $this.val(_val);
              wpcf7.triggerEvent( sp, 'cf7mls_af', { sp: sp, ip: $this, qf: qf, text: _val} );
            }
            qf.on("change", function (event) {
              event.preventDefault();
              var _val = $(this).val();
              sp.text(_val);
              $this.val(_val);
              wpcf7.triggerEvent( sp, 'cf7mls_af', { sp: sp, ip: $this, qf: qf, text: _val} );
            });
          }
        });
    });

    // Background Color Progress Bar
    $("form.wpcf7-form").each(function (index, el) {
      let id_form = $(el).find('.cf7mls_progress_bar').attr('data-id-form');
      var progress_bar_bg_color =  $(el).find('.cf7mls_progress_bar').attr('data-bg-color');
      $('head').append('<style id="cf7mls_style_progress_bar_' + id_form + '" type="text/css"></style>');
      if(progress_bar_bg_color && id_form) {
        cf7mls_color_bar(progress_bar_bg_color, id_form, el);
      }
    });

    jQuery(document).on(
      "click",
      "form.wpcf7-form input:checkbox.wpcf7-acceptance",
      function (event) {
        //event.preventDefault();
        var $this = jQuery(this);
        var parent_fieldset = $this.closest("fieldset.fieldset-cf7mls");
        if (parent_fieldset.length) {
          var acceptances = jQuery(parent_fieldset).find(
            "input:checkbox.wpcf7-acceptance"
          );
          if (acceptances.length) {
            cf7mls_toggle_next_btn(acceptances, parent_fieldset);
          }
        }
      }
    );

    $(document).on("click", ".cf7mls_next", function (event) {
      event.preventDefault();
      var $this = $(this);
      $this.addClass("sending");
      current_fs = $this.closest(".fieldset-cf7mls");
      next_fs = current_fs.next();

      //validation
      var form = $this.parent().closest("form.wpcf7-form");

      var fd = new FormData();
      $.each(form.find('input[type="file"]'), function (index, el) {
        fd.append($(el).attr("name"), $(el)[0].files[0]);
      });

      var other_data = form.serializeArray();
      $.each(other_data, function (key, input) {
        fd.append(input.name, input.value);
      });

      $.ajax({
          url: cf7mls_object.ajax_url + "?action=cf7mls_validation",
          type: "POST",
          data: fd,
          processData: false,
          contentType: false
        })
        .done(function (msg) {
          $this.removeClass("sending");
          var json = $.parseJSON(msg);

          /*
           * Insert _form_data_id if 'json variable' has
           */
          if (typeof json._cf7mls_db_form_data_id != "undefined") {
            if (!form.find('input[name="_cf7mls_db_form_data_id"]').length) {
              form.append(
                '<input type="hidden" name="_cf7mls_db_form_data_id" value="' +
                json._cf7mls_db_form_data_id +
                '" />'
              );
            }
          }

          if (!json.success) {
            var checkError = 0;
            //reset error messages
            current_fs
              .find(".wpcf7-form-control-wrap")
              .removeClass("cf7mls-invalid");
            current_fs.find(".cf7mls-invalid").removeClass("cf7mls-invalid");

            current_fs
              .find(".wpcf7-form-control-wrap .wpcf7-not-valid-tip")
              .remove();

            current_fs
              .find(".wpcf7-form-control-wrap .wpcf7-not-valid")
              .removeClass("wpcf7-not-valid");

            if (has_response) {
              current_fs
                .find(".wpcf7-response-output.wpcf7-validation-errors")
                .removeClass("wpcf7-validation-errors");
            } else {
              current_fs
                .find(".wpcf7-response-output.wpcf7-validation-errors")
                .remove();
            }

            $.each(json.invalid_fields, function (index, el) {
              if (
                current_fs.find('input[name="' + index + '"]').length ||
                current_fs.find('input[name="' + index + '[]"]').length ||
                current_fs.find('select[name="' + index + '"]').length ||
                current_fs.find('select[name="' + index + '[]"]').length ||
                current_fs.find('textarea[name="' + index + '"]').length ||
                current_fs.find('textarea[name="' + index + '[]"]').length ||
                current_fs.find('input[data-name="' + index + '"]').length ||
                current_fs.find('input[data-name="' + index + '[]"]').length
              ) {
                checkError = checkError + 1;

                //var controlWrap = $('.wpcf7-form-control-wrap.' + index, form);
                var controlWraps = [
                  $('[name="' + index + '"]', form).parent(),
                  $('[name="' + index + '[]"]', form).parent(),
                  $('[data-name="' + index + '"]', form).parent(),
                  $('[data-name="' + index + '[]"]', form).parent()
                ];
                $.each(controlWraps, function (i1, e1) {
                  var _c = "wpcf7-not-valid-tip";
                  if (e1.hasClass("form-group")) {
                    e1.addClass("has-error");
                    _c += " help-block";
                  }
                  e1.addClass("cf7mls-invalid");
                  e1.find("span.wpcf7-not-valid-tip").remove();
                  e1.find(".wpcf7-validates-as-required").addClass(
                    "wpcf7-not-valid"
                  );
                  if (e1.parents(".wpcf7-checkbox").length) {
                    e1.parents(".wpcf7-checkbox").after(
                      '<span role="alert" class="' +
                      _c +
                      '">' +
                      el.reason +
                      "</span>"
                    );
                  } else if (e1.parents(".wpcf7-radio").length) {
                    e1.parents(".wpcf7-radio").after(
                      '<span role="alert" class="' +
                      _c +
                      '">' +
                      el.reason +
                      "</span>"
                    );
                  } else {
                    e1.append(
                      '<span role="alert" class="' +
                      _c +
                      '">' +
                      el.reason +
                      "</span>"
                    );
                  }
                });

                //return false;
              }
            });

            if (checkError == 0) {
              json.success = true;
              has_response = false;
              // jQuery("html, body").animate(
              //   {
              //     scrollTop: jQuery($this.closest("form")).offset().top - 110
              //   },
              //   1000
              // );
            } else {
              if (current_fs.find(".wpcf7-response-output").length) {
                has_response = true;

                $icon = '';
                $icon += '<svg class="wpcf7-icon-wraning" width="18px" height="18px" x="0px" y="0px" viewBox="0 0 1000 1000" enable-background="new 0 0 1000 1000" xml:space="preserve">';
                $icon += '<g><path d="M499.9,361.6c-12.7,0-23,10.3-23,23v352.2c0,12.7,10.3,23,23,23s23-10.3,23-23V384.6C522.9,371.9,512.6,361.6,499.9,361.6z"/>';
                $icon += '<path d="M500.1,240.2c-12.7,0-23,10.3-23,23v30.6c0,12.7,10.3,23,23,23c12.7,0,23-10.3,23-23v-30.6C523.1,250.5,512.8,240.2,500.1,240.2z"/>';
                $icon += '<path d="M500,10C229.4,10,10,229.4,10,500c0,270.6,219.4,490,490,490c270.6,0,490-219.4,490-490C990,229.4,770.6,10,500,10z M500,944.1C254.8,944.1,55.9,745.2,55.9,500C55.9,254.8,254.8,55.9,500,55.9S944.1,254.8,944.1,500C944.1,745.2,745.2,944.1,500,944.1z"/></g></svg>';
                current_fs
                  .find(".wpcf7-response-output")
                  .addClass("wpcf7-validation-errors")
                  .show()
                  .html($icon + json.message);
              } else {
                has_response = false;
                $icon = '';
                $icon += '<svg class="wpcf7-icon-wraning" width="18px" height="18px" x="0px" y="0px" viewBox="0 0 1000 1000" enable-background="new 0 0 1000 1000" xml:space="preserve">';
                $icon += '<g><path d="M499.9,361.6c-12.7,0-23,10.3-23,23v352.2c0,12.7,10.3,23,23,23s23-10.3,23-23V384.6C522.9,371.9,512.6,361.6,499.9,361.6z"/>';
                $icon += '<path d="M500.1,240.2c-12.7,0-23,10.3-23,23v30.6c0,12.7,10.3,23,23,23c12.7,0,23-10.3,23-23v-30.6C523.1,250.5,512.8,240.2,500.1,240.2z"/>';
                $icon += '<path d="M500,10C229.4,10,10,229.4,10,500c0,270.6,219.4,490,490,490c270.6,0,490-219.4,490-490C990,229.4,770.6,10,500,10z M500,944.1C254.8,944.1,55.9,745.2,55.9,500C55.9,254.8,254.8,55.9,500,55.9S944.1,254.8,944.1,500C944.1,745.2,745.2,944.1,500,944.1z"/></g></svg>';

                current_fs.append(
                  '<div class="wpcf7-response-output wpcf7-display-none wpcf7-validation-errors" style="display: block;" role="alert">' + $icon + 
                    json.message +
                  "</div>"
                  

                );
              }
            }
          }

          if (json.success) {
            /*
                    current_fs.fadeOut('400', function() {
                        next_fs.fadeIn('400');
                    });
                    
                    });
                    */

            //reset error messages
            current_fs
              .find(".wpcf7-form-control-wrap")
              .removeClass("cf7mls-invalid");
            current_fs.find(".cf7mls-invalid").removeClass("cf7mls-invalid");
            current_fs.find(".wpcf7-not-valid").removeClass("wpcf7-not-valid");
            current_fs
              .find(".wpcf7-form-control-wrap .wpcf7-not-valid-tip")
              .remove();

            /*
             * Instead of hiding current fs, we hide all
             */
            /*
                    current_fs.css({
                        height: '0px',
                        overflow: 'hidden',
                        opacity: '0',
                        'visibility': 'hidden'
                    }).removeClass('cf7mls_current_fs');
                    */

            form.find(".cf7mls_current_fs").addClass("cf7mls_back_fs");

            form.find(".fieldset-cf7mls").removeClass("cf7mls_current_fs");

            next_fs.addClass("cf7mls_current_fs");
            
            if (form.find(".cf7mls_progress_bar").length) {
              let allow_choose_step =  form.find('.cf7mls_progress_bar').attr('data-allow-choose-step');
              let order_cur = Number(form.find('fieldset.cf7mls-choose-step').attr('data-cf7mls-order'));
              let step_cur = Number(form.find(".cf7mls_progress_bar li.current").attr('data-counter')) - 1;
              
              // allow choose step
              if(allow_choose_step === 'on') {
                form.find('fieldset.fieldset-cf7mls').css({display: ''});
                form.find("fieldset.fieldset-cf7mls").removeClass("cf7mls-choose-step");
              }

              if((allow_choose_step === 'on') && 
                ((order_cur !== step_cur) && ((order_cur === 0) || order_cur))
              ) {
                form.find("fieldset.fieldset-cf7mls").removeClass("cf7mls_back_fs");
                form.find("fieldset.fieldset-cf7mls").removeClass("cf7mls_current_fs");

                form.find('fieldset.fieldset-cf7mls').each(function( index, el ) {
                  if(index > step_cur) {
                    return;
                  }
                  $(el).addClass("cf7mls_back_fs");
                  if(index === step_cur) {
                    $(el).removeClass("cf7mls_back_fs");
                    $(el).addClass("cf7mls_current_fs");
                  }
                });
              }else {
                var cur = form.find("fieldset.fieldset-cf7mls").index(current_fs);
                var nex = form.find("fieldset.fieldset-cf7mls").index(next_fs);
                if(cf7mls_object.is_rtl == '1') {
                  cur = 0 - cur
                  nex = 0 - nex
                }
                form
                  .find(".cf7mls_progress_bar li")
                  .eq(cur)
                  .removeClass("current");
                form
                  .find(".cf7mls_progress_bar li")
                  .eq(nex)
                  .addClass("active current");
                
                cf7mls_step_item_finish(cur, nex, form, 'next');
                cf7mls_icon_check('next');
              }
            }
            

            // Progress Bar in ipad and mobie phone
            if(form.find(".cf7mls_number_step_wrap").length) {
              cf7mls_bar_process(form);
            }

            cf7mls_transition_effects(form, 'effects_next');

            dhScrollTo(form);
            return false;
          } else {}
        })
        .fail(function () {
          $this.removeClass("sending");
          console.log("Validation error");
        })
        .always(function () {
          $this.removeClass("sending");
          console.log("Validation complete");
        });

      return false;
    });

    $(".cf7mls_back").click(function () {
      var $this = $(this);
      var form = $this.parent().closest("form.wpcf7-form");

      $(".wpcf7-response-output.wpcf7-display-none")
        .removeClass("wpcf7-validation-errors")
        .removeAttr("style")
        .html("");
      $(".wpcf7-response-output.wpcf7-display-none.wpcf7-mail-sent-ok").hide();

      current_fs = $this.closest(".fieldset-cf7mls");
      previous_fs = current_fs.prev();

      //reset error messages
      current_fs.find(".wpcf7-form-control-wrap").removeClass("cf7mls-invalid");
      current_fs.find(".cf7mls-invalid").removeClass("cf7mls-invalid");
      current_fs.find(".wpcf7-not-valid").removeClass("wpcf7-not-valid");
      current_fs.find(".wpcf7-form-control-wrap .wpcf7-not-valid-tip").remove();

      /*
       * Instead of hide current fs, we hide all
       */
      /*current_fs.css({
                height: '0px',
                overflow: 'hidden',
                opacity: '0',
                'visibility': 'hidden'
            }).removeClass('cf7mls_current_fs');*/
      form.find(".fieldset-cf7mls").removeClass("cf7mls_current_fs");

      previous_fs.addClass("cf7mls_current_fs").removeClass("cf7mls_back_fs");

      if (form.find(".cf7mls_progress_bar").length) {
        form.find('fieldset.fieldset-cf7mls').css({display: ''});
        let allow_choose_step =  form.find('.cf7mls_progress_bar').attr('data-allow-choose-step');
        let order_cur = Number(form.find('fieldset.cf7mls-choose-step').attr('data-cf7mls-order'));
        let step_cur = Number(form.find(".cf7mls_progress_bar li.current").attr('data-counter')) - 1;

        if((allow_choose_step === 'on') && 
          ((order_cur !== step_cur) && ((order_cur === 0) || order_cur))
        ) {
          form.find("fieldset.fieldset-cf7mls").removeClass("cf7mls_back_fs");
          form.find("fieldset.fieldset-cf7mls").removeClass("cf7mls_current_fs");
          form.find("fieldset.fieldset-cf7mls").removeClass("cf7mls-choose-step");
          
          form.find('fieldset.fieldset-cf7mls').each(function( index, el ) {
            if(index > step_cur) {
              return;
            }
            $(el).addClass("cf7mls_back_fs");
            if(index === step_cur) {
              $(el).removeClass("cf7mls_back_fs");
              $(el).addClass("cf7mls_current_fs");
            }
          });
        }else {
          var pre = form.find("fieldset.fieldset-cf7mls").index(previous_fs)
          var cur = form.find("fieldset.fieldset-cf7mls").index(current_fs)
          if(cf7mls_object.is_rtl == '1') {
            pre = 0 - pre
            cur = 0 - cur
          }
          form
            .find(".cf7mls_progress_bar li")
            .eq(pre)
            .addClass("current");
          form
            .find(".cf7mls_progress_bar li")
            .eq(cur)
            .removeClass("active current");

          cf7mls_icon_check('back');
          cf7mls_step_item_finish(pre, cur, form, 'back');
        }
      }

      // Progress Bar in ipad and mobie phone
      if(form.find(".cf7mls_number_step_wrap").length) {
        cf7mls_bar_process(form);
      }

      cf7mls_transition_effects(form, 'effects_back');

      dhScrollTo(form);
      return false;
    });

    /*
     * Preview Form Clicked
     */
    $(document).on("click", ".wpcf7-cf7mls_preview_step", function (event) {
      event.preventDefault();
      var $this = $(this);
      var form = $this.closest("form.wpcf7-form");

      if (preview_clicked === false) {
        form.find(".cf7mls_back").css('display', 'none');
        form.find(".cf7mls_next").css('display', 'none');

        form.css('overflow', 'inherit');
        // form.find(".fieldset-cf7mls").css({
        //   height: "auto",
        //   overflow: "visible",
        //   opacity: "1",
        //   visibility: "visible"
        // });
        form.find("input").attr("disabled", "disabled");
        form.find("button").attr("disabled", "disabled");
        form.find("select").attr("disabled", "disabled");
        form.find("textarea").attr("disabled", "disabled");
        form.find(".wpcf7-cf7mls_preview_step").removeAttr("disabled");

        form.addClass("cf7mls_reviewing");
        $("body").append('<div class="cf7mls_reviewing_overlay"></div>');
        form.find('.fieldset-cf7mls').addClass('cf7mls_preview_fs');
      } else {
        form.css('overflow', '');
        // form.find(".fieldset-cf7mls").css({
        //   height: "",
        //   overflow: "",
        //   opacity: "",
        //   visibility: ""
        // });

        form.find(".cf7mls_back").css('display', '');
        form.find(".cf7mls_next").css('display', '');
        
        form.find('.fieldset-cf7mls').removeClass('cf7mls_preview_fs');

        form.find("input").removeAttr("disabled");
        form.find("button").removeAttr("disabled");
        form.find("select").removeAttr("disabled");
        form.find("textarea").removeAttr("disabled");

        form.removeClass("cf7mls_reviewing");
        $("body")
          .find(".cf7mls_reviewing_overlay")
          .remove();
      }

      preview_clicked = !preview_clicked;
    });
  });

  // Allow Choose Step
  $("form.wpcf7-form").each(function (index, el) {
    let style_bar = $(el).find('.cf7mls_progress_bar').attr('data-bg-style-bar');
    let step = '';
    if(style_bar == 'box_vertical_squaren' ||
      style_bar == 'box_larerSign_squaren' 
    ) {
      step = $('.cf7mls_progress_bar li'); 
    }else {
      step = $('.cf7mls_progress_bar li .cf7_mls_steps_item_icon');
    }
    step.click(function() {
      var allow_choose_step =  $(this).parents('.cf7mls_progress_bar').attr('data-allow-choose-step');
      if(allow_choose_step === 'on') {
        var form = $(this).parents("form.wpcf7-form");
        form.find('.wpcf7-response-output').css('display', '');
        form.find('.wpcf7-response-output').text('');
        let step_action = '';

        if(style_bar == 'box_vertical_squaren' ||
          style_bar == 'box_larerSign_squaren' 
        ) {
          step_action = Number($(this).attr('data-counter')) - 1;
        }else {
          step_action = Number($(this).parents('li').attr('data-counter')) - 1;
        }

        $(form.find('.fieldset-cf7mls-wrapper .fieldset-cf7mls')[step_action]).removeClass('cf7mls-choose-step');
        form.find('.fieldset-cf7mls-wrapper .fieldset-cf7mls').removeClass('cf7mls_back_fs');
        form.find('.fieldset-cf7mls-wrapper .fieldset-cf7mls').removeClass('cf7mls_current_fs');
        form.find('.fieldset-cf7mls-wrapper .fieldset-cf7mls').removeClass('cf7mls-choose-step');
        
        form.find('.fieldset-cf7mls-wrapper .fieldset-cf7mls').css({display: 'none'});
        $(form.find('.fieldset-cf7mls-wrapper .fieldset-cf7mls')[step_action]).addClass('cf7mls_current_fs');
        $(form.find('.fieldset-cf7mls-wrapper .fieldset-cf7mls')[step_action]).addClass('cf7mls-choose-step');
        $(form.find('.fieldset-cf7mls-wrapper .fieldset-cf7mls')[step_action]).css({display: ''});
      }
    })
  });

  //jQuery(window).on("load", function () {
    // jQuery.each(jQuery('form.wpcf7-form'), function(index, el) {
      // var bar_li = jQuery('.cf7mls_progress_bar li', jQuery(el));
      // bar_li.css({
      //     'width' : "calc(100% / " + bar_li.length + ")"
      // });
      // var le = jQuery('.cf7mls_progress_bar li', jQuery(el)).length;
      // jQuery.each(jQuery('.cf7mls_progress_bar li', jQuery(el)), function(index, el) {
      //   jQuery(el).attr('data-counter', index + 1);
      //   jQuery(el).attr('data-counter_rtl', le);
      //   le--;
      // });
    // });
  //});

  function cf7mls_is_not_last_fieldset(fieldset, total_fieldset) {
    var order = fieldset.data("cf7mls-order");
    return order != total_fieldset;
  }

  function dhScrollTo(el) {
    if (el.find(".fieldset-cf7mls-wrapper.no-scroll").length || el.hasClass('cf7mls-no-scroll')) {
      return;
    }
    if (cf7mls_object.scroll_step == "true") {
      $("html, body").animate({
          scrollTop: el.offset().top - 110
        },
        "slow"
      );
    } else if (cf7mls_object.scroll_step == "scroll_to_top") {
      $("html, body").animate({
          scrollTop: $("body").offset().top - 110
        },
        "slow"
      );
    }
  }

  function cf7mls_toggle_next_btn(acceptances, fieldset) {
    if (acceptances.length > 0) {
      var ii = 0;
      jQuery.each(acceptances, function (i, v) {
        if (jQuery(v).is(":checked")) {
          //console.log('checked');
        } else {
          ii++;
        }
      });
      if (ii > 0) {
        //console.log(ii);
        jQuery(fieldset)
          .find(".cf7mls_next")
          .attr("disabled", "disabled");
      } else {
        jQuery(fieldset)
          .find(".cf7mls_next")
          .removeAttr("disabled");
      }
    }
  }

  // show, hide icon check
  function cf7mls_icon_check(event) {
    if(event == 'next') {
      $('.cf7mls_progress_bar li').each(function(key, el) { 
        if(($(el).hasClass('active')) && !($(el).hasClass('current'))) {
          $($(el).find('.cf7_mls_count_step')).css('display', 'none');
          $($(el).find('.cf7_mls_check')).css('display', 'block');
        }
      })
    }

    if(event == 'back') {
      $('.cf7mls_progress_bar li').each(function(key, el) { 
        if(!($(el).hasClass('active')) || ($(el).hasClass('current'))) {
          $($(el).find('.cf7_mls_count_step')).css('display', 'block');
          $($(el).find('.cf7_mls_check')).css('display', 'none');
        }
      })
    }
  }

  // add, remove class step item finish
  function cf7mls_step_item_finish (cur, nex, form, event) {
    let style_text = form.find('.cf7mls_progress_bar').attr('data-style-text');
    let style_bar = form.find('.cf7mls_progress_bar').attr('data-bg-style-bar');
    /*
      note: cur start  form 0, nex start form 1.
    */
    let numberItem;
    if(style_text == 'horizontal' || style_text == 'no') {
      if((style_bar == 'navigation_horizontal_squaren') || 
        (style_bar == 'navigation_horizontal_round') ||
        (style_bar == 'largerSign_squaren') ||
        (style_bar == 'largerSign_round')
      ) {
        numberItem = cur;
      }
    }

    if(style_text == 'vertical') {
      if((style_bar == 'navigation_horizontal_squaren') ||
          (style_bar == 'navigation_horizontal_round') ||
          (style_bar == 'largerSign_squaren') ||
          (style_bar == 'largerSign_round')
        ) {
          numberItem = nex;
        }
    }

    if((style_bar == 'box_vertical_squaren') || 
      (style_bar == 'box_larerSign_squaren')) 
    {
      numberItem = cur;
    }

    if((style_bar == 'horizontal_round') || 
      (style_bar == 'horizontal_squaren')
    ) {
      numberItem = nex;
    }
    
    if(numberItem || numberItem == '0') {
      if(event == 'next') {
        form
          .find(".cf7mls_progress_bar li")
          .eq(numberItem)
          .addClass("cf7mls-steps-item-finish");
      }else if(event == 'back') {
        form
          .find(".cf7mls_progress_bar li")
          .eq(numberItem)
          .removeClass("cf7mls-steps-item-finish");
      }

    }
  }

  function cf7mls_color_bar(color, id_form, el) {
    let style_bar = 'cf7mls_bar_style_' + $(el).find('.cf7mls_progress_bar').attr('data-bg-style-bar');
    let style_text = 'cf7mls_bar_style_text_' + $(el).find('.cf7mls_progress_bar').attr('data-style-text');

    let css_item_icon = '.' + style_bar + '.' + style_text + '[data-id-form="'+ id_form +'"]' + ' li.active .cf7_mls_steps_item_icon { background: '+ color + ';}';
    let css_item_icon_befor = '.' + style_bar + '.' + style_text + '[data-id-form="'+ id_form +'"]' + ' li.active:before { background: '+ color + ';}';
    let css_bg_li = '.' + style_bar + '.' + style_text + '[data-id-form="'+ id_form +'"]' + ' li.active{ background: '+ color + ';}';
    let css_step = '.' + style_bar + '.' + style_text + '[data-id-form="'+ id_form +'"]' + ' li.active .cf7_mls_count_step{ color: '+ color + ';}'
    let css_check = '.' + style_bar + '.' + style_text + '[data-id-form="'+ id_form +'"]' + ' li.active .cf7_mls_check{ color: '+ color + ';}';
    let css_li_after = '.' + style_bar + '.' + style_text + '[data-id-form="'+ id_form +'"]' + ' li.active:after{background: '+ color + ';}';
    let css_active_title  = '.' + style_bar + '.' + style_text + '[data-id-form="'+ id_form +'"]' + ' li.active .cf7mls_progress_bar_title{color: #fff;}';
    let classItemFinsish = '.' + style_bar + '.' + style_text + '[data-id-form="'+ id_form +'"]' + ' li.cf7mls-steps-item-finish';
    let classCurrent = '.' + style_bar + '.' + style_text + ' li.current';
    let css_title_after = '.cf7mls_progress_bar_title:after{background: '+ color + ';}';
    let css_title_border = '.cf7mls_progress_bar_title:after{border-color: '+ color + ';}';
    let css_li_cur = '.' + style_bar + '.' + style_text + ' li.current + li:after{ background: '+ color + ';}';

    let css_progress_bar = '';
    // progress bar on computer
    if((style_bar == 'cf7mls_bar_style_navigation_horizontal_squaren') ||
    (style_bar == 'cf7mls_bar_style_largerSign_squaren') ||
    (style_bar == 'cf7mls_bar_style_navigation_horizontal_round') ||
    (style_bar == 'cf7mls_bar_style_largerSign_round')
    ) {
      switch (style_text) {
        case 'cf7mls_bar_style_text_horizontal': 
          css_progress_bar += css_item_icon;

          if((style_bar == 'cf7mls_bar_style_navigation_horizontal_squaren') || 
            (style_bar == 'cf7mls_bar_style_navigation_horizontal_round')
          ) {
            css_progress_bar += classItemFinsish + ' ' + css_title_after; 
          }

          if((style_bar == 'cf7mls_bar_style_largerSign_squaren') || 
            (style_bar == 'cf7mls_bar_style_largerSign_round')
          ) {
            css_progress_bar += classItemFinsish + ' ' + '.cf7_mls_arrow_point_to_righ svg {fill: '+ color + ';}';
          }

          break; 

        case 'cf7mls_bar_style_text_vertical': 
          css_progress_bar += css_item_icon_befor;

          if((style_bar == 'cf7mls_bar_style_navigation_horizontal_squaren') ||
            (style_bar == 'cf7mls_bar_style_navigation_horizontal_round')
          ) {
            css_progress_bar += classItemFinsish + ':after{ background: '+ color + ';}'; 
          }

          if((style_bar == 'cf7mls_bar_style_largerSign_squaren') ||
            (style_bar == 'cf7mls_bar_style_largerSign_round')
          ) {
            css_progress_bar += classItemFinsish + ':after{ border-color: '+ color + ';}';
          }
          
          break; 

        case 'cf7mls_bar_style_text_no': 
          css_progress_bar += css_item_icon;

          if((style_bar == 'cf7mls_bar_style_navigation_horizontal_squaren') ||
            (style_bar == 'cf7mls_bar_style_navigation_horizontal_round')
          ) {
            css_progress_bar += classItemFinsish + ' ' + css_title_after; 
          }

          if((style_bar == 'cf7mls_bar_style_largerSign_squaren') ||
            (style_bar == 'cf7mls_bar_style_largerSign_round')
          ) {
            css_progress_bar += classItemFinsish + ' ' + css_title_border; 
          }
          break; 
      }
    }
    
    if((style_bar == 'cf7mls_bar_style_horizontal_squaren') ||
        (style_bar == 'cf7mls_bar_style_horizontal_round')  
    ) {
      if(style_text == 'cf7mls_bar_style_text_horizontal') {
        css_progress_bar += css_item_icon;
        css_progress_bar += classCurrent + ':before {background-color:' + color + '}';
      }

      if((style_text == 'cf7mls_bar_style_text_vertical') || 
        (style_text == 'cf7mls_bar_style_text_no')) {
        css_progress_bar += css_item_icon_befor;
        css_progress_bar += classCurrent + ':after {background-color:' + color + '}';
      }
    }
    
    if(((style_bar == 'cf7mls_bar_style_box_vertical_squaren') || 
      (style_bar == 'cf7mls_bar_style_box_larerSign_squaren')) && 
      (style_text)
    ) {
      css_progress_bar += css_bg_li;
      css_progress_bar += css_step;
      css_progress_bar += css_check;
      css_progress_bar += css_li_after; 
      css_progress_bar += css_active_title;
    }

    if(style_bar == 'cf7mls_bar_style_box_larerSign_squaren') {
      css_progress_bar += css_li_cur;
    }

    jQuery('style#cf7mls_style_progress_bar_' + id_form).text(css_progress_bar);
  }

  // progress bar in ipad and mobie phone
  function cf7mls_bar_process(form) {
    let number_step_cur = form.find('.cf7mls_progress_bar li.current').attr('data-counter'); 
    let number_step = form.find('.cf7mls_number_step_wrap').attr('data-number-step');
    let bg_color = form.find('.cf7mls_number_step_wrap').attr('data-bg-color');
    if(number_step_cur && number_step) {
      form.find('.cf7mls_number_step_wrap .cf7mls_number').text(number_step_cur + '/' + number_step);
      let title = $(form.find('.cf7mls_progress_bar li')[Number(number_step_cur) - 1]).find('.cf7mls_progress_bar_title').text();
      form.find('.cf7mls_number_step_wrap .cf7mls_step_current').text(title);
      let percent_step = 100 / (Number(number_step) - 1);
      if(number_step_cur == '1') {
        form.find('.cf7mls_number_step_wrap .cf7mls_progress_barinner').css('width', '');
      }else {
        form.find('.cf7mls_number_step_wrap .cf7mls_progress_barinner').css('width', ((percent_step * (Number(number_step_cur) - 1)) + '%'));
      }
    }

    if(bg_color) {
      form.find('.cf7mls_number_step_wrap .cf7mls_progress_barinner').css('background', bg_color);
    }
  }

  function cf7mls_transition_effects(form, transitions_bt) {
    var transition_effects = $(form).find(".fieldset-cf7mls-wrapper").attr("data-transition-effects");
    if(transition_effects && typeof transition_effects !== undefined) {
      var effects  = transition_effects.split(" ");
      var effect_form = {
        transition_effects: transition_effects,
        effects_back: '',
        effects_next: '',
        effects_in: ''
      };

      jQuery.each(effects, function(index, effect){
        var es = effect.split("_");

        switch(es[0]) {
          case 'back':
            effect_form.effects_back = es[1];
            break;
          case 'next':
            effect_form.effects_next = es[1];
            break;
          case 'in':
            effect_form.effects_in = es[1];
            break;
        }
      })

      if(transitions_bt == 'effects_in') {
        $(form).find('.fieldset-cf7mls-wrapper .cf7mls_current_fs').addClass(effect_form.effects_in + ' ' +"animated");
      }else if(form.find(".fieldset-cf7mls-wrapper").length && transitions_bt) {
        form.find(".fieldset-cf7mls-wrapper .fieldset-cf7mls").removeClass(effect_form.effects_back);
        form.find(".fieldset-cf7mls-wrapper .fieldset-cf7mls").removeClass(effect_form.effects_next);
        form.find(".fieldset-cf7mls-wrapper .fieldset-cf7mls").removeClass(effect_form.effects_in);
        form.find(".fieldset-cf7mls-wrapper .fieldset-cf7mls").removeClass('animated');
        form.find(".fieldset-cf7mls-wrapper .cf7mls_current_fs").addClass(effect_form[transitions_bt] + ' ' + "animated");
      }
    }
  }

})(jQuery);