/*!
 * Lush Content Slider
 * http://geedmo.com
 *
 * Version: 1.7.3
 * Author: @geedmo
 * Copyright (c) 2014, Geedmo. All rights reserved.
 * Released under CodeCanyon Regular License: http://codecanyon.net/licenses
 *
 * News: http://codecanyon.net/user/geedmo/portfolio
 * ======================================================= */

;(function ( $, window, document, undefined ) {


    /**
     *  Plugin Helpers
     *******************************/
    $.fn.forceReflow = function(){
      return this.each(function(){
        var reflow = this.offsetWidth;
      });
    };

    $.fn.clearState = function(state){
      return this.removeClass( (this.data('activeClass') || '') + ' ' + state + ' live')
    };

    $.fn.prepareEffect = function(duration, easing){
      return this.each(function(){
        var $this = $(this),
            animation = {};
        if($this.css($.support.css3feature.animation.name+'FillMode') === 'both') {
          animation[$.support.css3feature.animation.name+'Duration'] = duration + 'ms'
          animation[$.support.css3feature.animation.name+'TimingFunction'] = easing
          $this.clearTransition().css(animation)
        }
        else {
          var transition = {};
          // separate transitions property
          transition[$.support.css3feature.transition.name+'Property'] = 'all';
          transition[$.support.css3feature.transition.name+'Duration'] = duration + 'ms';
          transition[$.support.css3feature.transition.name+'TimingFunction'] = easing;
          transition[$.support.css3feature.transition.name+'Delay'] = '0s'

          $this.css(transition)
        }
      });
    };

    $.fn.clearTransition = function() {
        var cleared = {};
            cleared[$.support.css3feature.transition.name+'Duration'] = '0s'
            cleared[$.support.css3feature.transition.name] = 'none'
        return this.css(cleared);
    }

    /**
     *  Plugin Globals
     *******************************/

    var pluginName      = 'lush',
        sliderClass     = 'lush-slider',
        flexsliderClass = 'flexslider',
        containerClass  = 'lush',
        classPrev       = 'lush-prev',
        classNext       = 'lush-next',
        classPage       = 'lush-page',
        classNav        = 'lush-nav',
        classShadow     = 'lush-shadow',
        classExternal   = 'lush-external',
        sliderData      = 'lushSlider',
        flexsliderData  = 'lushFlexslider',
        fadeMargin      = 50;



    function Lush( element, option ) {

        /* CSS TRANSITION SUPPORT (http://www.modernizr.com/)
         * - run here when document is ready
         * ======================================================= */
        $.support.css3feature=(function(){var b=document.createElement("lush"),d=(function(){var f={WebkitTransition:"webkitTransitionEnd",MozTransition:"transitionend",OTransition:"oTransitionEnd otransitionend",transition:"transitionend"},e;for(e in f){if(b.style[e]!==undefined){return{end:f[e],name:e}}}}()),c=(function(){var f={WebkitAnimation:"webkitAnimationEnd",MozAnimation:"animationend",OAnimation:"oAnimationEnd",MSAnimation:"MSAnimationEnd",animation:"animationend"},e;for(e in f){if(b.style[e]!==undefined){return{end:f[e],name:e}}}}());b=null;return (d || c) && {transition:d,animation:c}})();


        // a footprint to know that we have already started
        $.data(element, pluginName, this);

        this.container = $(element);
        this.elements  = this.container.children().not('.ignore, .lush-nav');

        this.options = option;
        this.options.manual = false;

        // attempt to set height before start
        this.container.height(
          this.container.width() / (this.options.baseWidth / this.options.baseHeight)
          );

        this.sliding     = false;   // lock a slide when doing animations
        this.stopped     = false;   // slider stopped and needs to advance
        this.paused      = false;   // global paused state
        this.outRendered = false;   // to check if animation out was rendered

        // ensure properties as number
        this.options.deadtime = isNaN(parseInt(this.options.deadtime)) ? 0 : parseInt(this.options.deadtime);

        // carousel only works with slider mode
        if( ! this.options.isSlider && this.options.carousel)
            this.options.carousel = false;

        // translate classic easing function to css3 cubic-bezier
        this.cssEasing = {
          'linear':         'linear',
          'swing':          'ease-out',
          'ease':           'ease',
          'ease-in':        'ease-in',
          'ease-out':       'ease-out',
          'ease-in-out':    'ease-in-out',
          'snap':           'cubic-bezier(0,1,.5,1)',
          'easeOutCubic':   'cubic-bezier(.215,.61,.355,1)',
          'easeInOutCubic': 'cubic-bezier(.645,.045,.355,1)',
          'easeInCirc':     'cubic-bezier(.6,.04,.98,.335)',
          'easeOutCirc':    'cubic-bezier(.075,.82,.165,1)',
          'easeInOutCirc':  'cubic-bezier(.785,.135,.15,.86)',
          'easeInExpo':     'cubic-bezier(.95,.05,.795,.035)',
          'easeOutExpo':    'cubic-bezier(.19,1,.22,1)',
          'easeInOutExpo':  'cubic-bezier(1,0,0,1)',
          'easeInQuad':     'cubic-bezier(.55,.085,.68,.53)',
          'easeOutQuad':    'cubic-bezier(.25,.46,.45,.94)',
          'easeInOutQuad':  'cubic-bezier(.455,.03,.515,.955)',
          'easeInQuart':    'cubic-bezier(.895,.03,.685,.22)',
          'easeOutQuart':   'cubic-bezier(.165,.84,.44,1)',
          'easeInOutQuart': 'cubic-bezier(.77,0,.175,1)',
          'easeInQuint':    'cubic-bezier(.755,.05,.855,.06)',
          'easeOutQuint':   'cubic-bezier(.23,1,.32,1)',
          'easeInOutQuint': 'cubic-bezier(.86,0,.07,1)',
          'easeInSine':     'cubic-bezier(.47,0,.745,.715)',
          'easeOutSine':    'cubic-bezier(.39,.575,.565,1)',
          'easeInOutSine':  'cubic-bezier(.445,.05,.55,.95)',
          'easeInBack':     'cubic-bezier(0.6,-0.28,0.735,0.045)',
          'easeOutBack':    'cubic-bezier(.175, .885,.32,1.275)',
          'easeInOutBack':  'cubic-bezier(.68,-.55,.265,1.55)'
        }

        // hidden until starts
        this.container.css({visibility : 'hidden'})

        if(this.options.isSlider)
          this.container.hide();

        this.preload(this.container, $.proxy(this.init, this));
    }

    Lush.prototype = {

      init: function() {
          var prevTimeOut = 0,
              prevTimeIn  = 0,
              oldDisplay,
              self = this;

          if ( ! this.container.hasClass('lush') )
            this.container.addClass('lush')

          this.container.css({visibility : 'visible'})

          this.updatePos();

          // flex slider fade animation
          if(this.options.flexslider) {
            oldDisplay = this.container.css('display');
            this.container.show()
          }

          if(this.options.isSlider)
            this.container.show()

          $.each(this.elements, $.proxy(function(i, element){

              // e :   the current element
              // origin: where to get the slide data
              // $el:    the jQueryzed element
              // origin: auxiliar to save element data
              var e = this.elements[i].$el = $(element),
                  origin;

              /////// SLIDE IN DATA

              e.slideIn = {};
              e.slideOut = {};

              // get data from element if set, then from container
              origin = e.data('slide-in') || self.container.data('slide-in')

              if(origin)
                  e.dataIn = origin.split(' '); // split on space

              // Elements in - property value
              e.slideIn.at     = parseInt(this.get('at', e.dataIn));
              e.slideIn.from   = this.get('from', e.dataIn);
              e.slideIn.use    = this.get('use', e.dataIn);
              e.slideIn.during = parseInt(this.get('during', e.dataIn));
              e.slideIn.plus   = parseInt(this.get('plus', e.dataIn));
              e.slideIn.force  = this.get('force', e.dataIn);

              if(!this.cssEasing[e.slideIn.use])
                  e.slideIn.use = 'linear';

              if(e.slideIn.plus > 0)
                e.slideIn.at += e.slideIn.plus + prevTimeIn;

              prevTimeIn = e.slideIn.at;

              /////// SLIDE OUT DATA

              // get data from element if set, then from container
              origin = e.data('slide-out') || self.container.data('slide-out')

              if(origin) { // split on space
                  e.dataOut = origin.split(' ');

                  // Elements out - property value
                  e.slideOut.at     = parseInt(this.get('at', e.dataOut));
                  e.slideOut.to     = this.get('to', e.dataOut);
                  e.slideOut.use    = this.get('use', e.dataOut);
                  e.slideOut.during = parseInt(this.get('during',e.dataOut));
                  e.slideOut.plus   = parseInt(this.get('plus', e.dataOut));
                  e.slideOut.force  = this.get('force', e.dataOut);

                  if(!this.cssEasing[e.slideOut.use])
                      e.slideOut.use = 'linear';

                  if(e.slideOut.plus > 0)
                    e.slideOut.at += e.slideOut.plus + prevTimeOut;

                  prevTimeOut = e.slideOut.at;

              }

              // make sure all elements are absolute
              e.css({ 'position': 'absolute' })

              e = null;

          }, this))

          this.saveSize();


          //this.elements.filter('img').css('width','auto');

          if(this.options.flexslider)
            this.container.css('display', oldDisplay);

          if(this.options.isSlider)
              this.container.hide();

          // save default direction
          if(this.options.carousel)
            this.container.parent().data('from-direction',this.options.direction);


          if ( this.options.autostart )
              this.start();

          self.runHook('onInit');

          this.container.trigger('lushInit');

          // responsive handler
          $(window).resize($.proxy(this.resize, this));

      },

      /* *************************************
       * GET TIMELINE INFORMATION
       * *************************************/
      get: function(prop, data) {
          var pos = $.inArray(prop, data);

          // if not exists a property, use default
          if(pos < 0)
              return this.options.param[prop];
          // found attribute, return value
          // attributes without parameter are undefined when found
          return data[pos + 1] || !data[pos + 1];
      },

      /* *************************************
       * PREPARE TO RENDER IN ANIMATIONS
       * *************************************/
       renderIn: function(){
            var self = this,
                isInverted = this.carouselInvert(),
                elementCount = this.elements.length;

            this.container.addClass('running');

            this.elements.each($.proxy(function(index, element) {

                var el = element.$el;

                el.clearQueue();

                el.delay(parseInt( isInverted ? self.elements[--elementCount].$el.slideIn.at : el.slideIn.at ))

                // Queue In Animations
                this.from(el);

                el.queue( function(){

                  self.runHook('onItemSlideIn', el);

                  $(this).dequeue();

                });

                // if last item
                if((index == this.elements.length-1)) {
                  el.queue( function(){

                        self.runHook('onSlideIn');

                        self.container.trigger('slideIn');

                        $(this).dequeue();
                    });
                }

                // add an extra delay before start slide out
                if(this.options.deadtime > 0 && !el.slideOut.force)
                  el.delay(this.options.deadtime)

                if ($.support.css3feature)
                  el.show()

            }, this))
            return this;
      },

      /* *************************************
       * PREPARE TO RENDER OUT ANIMATIONS
       * *************************************/
       renderOut: function() {
            var self = this,
                isInverted = this.carouselInvert(),
                elementCount = this.elements.length;

            //this.container.addClass('running');

            // controls if out animationa has been rendered
            this.outRendered = true;

            // flag when out animations has been started
            this.outStarted = false;

            this.elements.each($.proxy(function(index, element){
                var el = element.$el, interval;

                if(el.slideOut.at >= 0) {

                  el.delay(parseInt( isInverted ? self.elements[--elementCount].$el.slideOut.at : el.slideOut.at ))

                  el.queue(function() {
                    if(self.paused && !el.slideOut.force && !self.outStarted)
                      interval = setInterval($.proxy(function() {
                        if(!self.paused) {
                          clearInterval(interval)
                          $(this).dequeue()
                      }
                    }, this), 50)
                    else {
                      $(this).dequeue()
                      if(!el.slideOut.force) self.outStarted = true;
                    }

                  })

                  // Queue Out Animations
                  this.to(el);

                  el.queue( function(){
                    self.runHook('onItemSlideOut', el);

                    $(this).dequeue();

                  });

                  if ((index == this.elements.length-1)) {
                    el.queue(function(){

                        self.runHook('onSlideOut');
                        self.container.trigger('slideOut');

                        $(this).dequeue()

                      });
                  }

                } // slideout.at

            }, this)) // proxy

            return this;
        },

        /* *************************************
         * START ANIMATING A NEW SLIDE
         * *************************************/
        start: function() {
            var self = this;

            if(this.sliding) return;

            this.sliding = true;

            this.container.show();

            this.container.addClass('active');

            this.resize();

            self.runHook('onSlide');
            this.container.trigger('slideStart')

            // render in animations
            this.renderIn();

            // if not manual advance
            // render out animations

            if( ! this.options.manual ) {

              this.renderOut();

            }

            this.end();

            // save default direction
            if(this.options.carousel)
              this.container.parent().data('from-direction',this.options.direction);

        },

        /* *************************************
         * DETECTS WHEN A SLIDE ENDS
         * @halt: slider stopped but doesn't need to advance
         * *************************************/
        end: function(halt) {
            var that = this;

            $.when(this.elements).done($.proxy(function() {

              if (!this.outRendered) {
                this.container.removeClass('running')
                //this.container.trigger('slideStop');
                return;
              }

              this.outRendered = false;

              this.endslide(halt);

            }, this ));

            return this;
        },

        /* *************************************
         * CLEAR SLIDING STATUS
         * @halt: slider stopped but doesn't need to advance
         * *************************************/
        endslide: function(halt) {

            var self = this;

            this.sliding = false;

            self.runHook('onSlided');
            this.container.removeClass('active running').trigger('slideEnd');

            // if in slider mode and not forced to stop and no halt
            if ( this.options.isSlider && !this.stopped && !halt )
                this.advance();

            this.stopped = false;
        },

        /* *************************************
         * ADVANCE TO GIVEN DIRECTION
         * *************************************/
        advance: function(direction) {
            var nextDirection = direction || this.options.direction,
                nextSlide;

            // not advance if slide in progress
            if ( ! this.sliding ) {

              nextSlide = (nextDirection == 'next') ? this.options.syncNext : this.options.syncPrev;
              $(nextSlide).lush('start');

            }
        },

        /* *************************************
         * SLIDE IFRAME & IMAGE PRELOAD
         * *************************************/
        preload: function(el, callback) {

            var preSrc = [],
                imgcnt = 0

            this.container.find('*').each(function(i, el){
                var $this = $(el), bg, src;
                // preload image tag
                if($this[0].tagName === 'IMG') {
                    src = {src : $this.attr('src'), tag : $this[0].tagName};
                    preSrc.push(src);
                } else if($this[0].tagName === 'IFRAME') {
                    src = {src : $this.attr('src'), tag : $this[0]};
                    preSrc.push(src);
                } else { // preload elements with url as bg image
                    bg = $this.css('background-image');
                    if( bg && bg !== 'none' && bg.indexOf('url') >= 0 ) {
                      src = { src: bg.match(/url\((.*)\)/)[1].replace(/"/gi, ''), tag: 'IMG' };
                      preSrc.push(src);
                    }
                }
            })

            if ( ! preSrc.length) {
                callback();
            } else {
                $.each(preSrc, function(i, src) {

                    if(src.tag === 'IMG')
                      $('<'+src.tag+'>').load(function() {
                          if( ++imgcnt == preSrc.length )
                               callback();
                      }).attr('src', src.src);
                    else
                      $(src.tag).load(function() {
                          if( ++imgcnt == preSrc.length )
                              callback();
                      }).attr('src', src.src);
                });
            }

        },

        /* *************************************
         * FORCE TO STOP ANIMATION
         * *************************************/
        stop: function() {
            this.stopped = true; // stops auto advance
            this.elements.each(function(i, element){
                while (element.$el.queue().length)
                    element.$el.stop(false, (!$.support.css3feature)); // jump to end when using fallbacks
            });
            return this;
        },

        /* *************************************
         * SLIDE TO DIRECTION
         * *************************************/
        go: function(direction) {
          var that = this;

          if(this.options.carousel)
            this.container.parent().data('from-direction',direction);

          if(this.options.manual) {

            if(this.outRendered) return;

            this.renderOut().end()

          }
          else {

            this.state('resume').stop().advance(direction);

          }

        },

        /* *************************************
         * PAUSED - RESUMED STATE
         * *************************************/
        state: function(state) {

          this.paused = (state === 'pause');
          if(this.paused)
            this.container.addClass('paused');
          else {
            this.container.removeClass('paused');
          }
          return this;
        },

        /* *************************************
         * RETURNS THE CONTAINER SIZE
         * *************************************/
        size: function() {
          return {
            width: this.container.width(),
            height: this.container.height()
          }
        },

        /* *************************************
         * HIDE ALL ELEMENTS IN A SLIDE
         * *************************************/
        hide: function(){
            this.elements.hide();
        },

        /* *************************************
         * SHOW ALL ELEMENTS IN A SLIDE
         * *************************************/
        show: function(){
            this.elements.show();
        },

        /* *************************************
         * SAVE ORIGINAL SIZES
         * *************************************/
        saveSize: function() {
          var properties = {};

          // save originaal container size
          this.containerSize = {
            width: this.options.baseWidth,
            height: this.options.baseHeight
          }

          this.elements.each(function(i, element){
            var $el =  $(element);
            // font
            properties.fs = parseInt($el.css('font-size') ,0) || 0;
            properties.lh = parseInt($el.css('line-height')) || 0;

            // padding
            properties.pt = parseInt($el.css('paddingTop')   ,0) || 0;
            properties.pb = parseInt($el.css('paddingBottom'),0) || 0;
            properties.pl = parseInt($el.css('paddingLeft')  ,0) || 0;
            properties.pr = parseInt($el.css('paddingRight') ,0) || 0;
            // margin
            properties.mt = parseInt($el.css('marginTop')   ,0) || 0;
            properties.mb = parseInt($el.css('marginBottom'),0) || 0;
            properties.ml = parseInt($el.css('marginLeft')  ,0) || 0;
            properties.mr = parseInt($el.css('marginRight') ,0) || 0;
            // border
            properties.btw = parseInt($el.css('borderTopWidth')   ,0) || 0;
            properties.bbw = parseInt($el.css('borderBottomWidth'),0) || 0;
            properties.blw = parseInt($el.css('borderLeftWidth')  ,0) || 0;
            properties.brw = parseInt($el.css('borderRightWidth') ,0) || 0;

            properties.bts = $el.css('borderTopStyle');
            properties.bbs = $el.css('borderBottomStyle');
            properties.bls = $el.css('borderLeftStyle');
            properties.brs = $el.css('borderRightStyle');

            properties.btc = $el.css('borderTopColor');
            properties.bbc = $el.css('borderBottomColor');
            properties.blc = $el.css('borderLeftColor');
            properties.brc = $el.css('borderRightColor');
            //size

            properties.hg = parseInt($el.height()) || properties.lh || 0;
            properties.wd = parseInt($el.width())  || 0;

            properties.b = $el.css('bottom');
            properties.l = $el.css('left');
            properties.r = $el.css('right');

            $el.data('properties', $.extend({}, properties));

          })
        },

        updatePos: function() {
              var self = this;
              this.elements.each(function(i, element){
                var $el =  $(element);

          if(!self.isUnit(element.style.left, '%'))
            $el.css('left', (parseFloat(element.style.left) * 100 / self.options.baseWidth) + '%');

          if(!self.isUnit(element.style.top, '%'))
            $el.css('top',(parseFloat(element.style.top) * 100 / self.options.baseHeight) + '%');

          })
        },

        isUnit: function (value, unit) {
          return ((value.indexOf(unit) > 0) || (unit == 'px' || value == 'auto'));
        },

        /* *************************************
         * SET NEW SIZE BY RESIZE RATIO
         * *************************************/
        resize: function() {
          var properties, ratio, $el;

          if(!this.containerSize) return; // bugix
          ratio = this.container.width() / this.containerSize.width;


          this.container.css({
              height: this.containerSize.height * ratio
              });

          if(this.options.isSlider || this.options.flexslider) {

            this.container.parent().css({
                height: this.containerSize.height * ratio
                });

          }

          this.elements.each(function(i, element) {
            $el = $(element);
            properties = $el.data('properties');

            if(!properties)
                return false;

            $el.css({
               'font-size':     (Math.floor(properties.fs * ratio)) + "px",
               'line-height':   lhUnitless(Math.floor(properties.lh * ratio)),

               'padding-top':   (properties.pt * ratio) + "px",
               'padding-bottom':(properties.pb * ratio) + "px",
               'padding-left':  (properties.pl * ratio) + "px",
               'padding-right': (properties.pr * ratio) + "px",
               /*
               'margin-top':    (properties.mt * ratio) + "px",
               'margin-bottom': (properties.mb * ratio) + "px",
               'margin-left':   (properties.ml * ratio) + "px",
               'margin-right':  (properties.mr * ratio) + "px",
               */
               'border-top':    (properties.btw * ratio) + "px " + properties.bts + ' ' + properties.btc,
               'border-bottom': (properties.bbw * ratio) + "px " + properties.bbs + ' ' + properties.bbc,
               'border-left':   (properties.blw * ratio) + "px " + properties.bls + ' ' + properties.blc,
               'border-right':  (properties.brw * ratio) + "px " + properties.brs + ' ' + properties.brc,

               'height':        (properties.hg * ratio) + 'px',
               'width':         (properties.wd * ratio) + 'px'
               //'white-space':   'nowrap'
             });

            if(element.tagName === 'IFRAME')
              $el.attr({
                width: (properties.wd * ratio),
                height: (properties.hg * ratio)
              })

          });
          /*return line height unitless when reaches less than 1 unit */
          function lhUnitless(val) { return (val<1) ? 1 : (val+'px'); }
        },

        /* *************************************
         * RETURN IF DIRECTION WAS INVERTED
         * *************************************/

        carouselInvert: function() {
          var fromdir = this.container.parent().data('from-direction');

          return ( this.options.carousel && fromdir &&
               fromdir !== this.options.direction )
        },

        /* *************************************
         * ANIMATE FROM DIRECTION
         * *************************************/
        from: function(el) {
            var objFrom, objTo,
              justFade = false,
              self   = this,
              effect;

            effect = this.carouselInvert() ?
            el.slideOut.to :
            el.slideIn.from;

            if ($.support.css3feature) {
              el.clearTransition()
                .clearState('out')
                .addClass('in')
                .data('activeClass', effect)
                .addClass(effect)

              el.prepareEffect(el.slideIn.during, self.cssEasing[el.slideIn.use])
                .queue( function() {
                  this.offsetWidth // reflow
                  $(this)
                    .addClass('live')
                    .dequeue();
                })
                .delay(parseInt(el.slideIn.during)-100)
            }
            else {

              switch(effect) {
                  case 'left':
                  case 'l':
                    objFrom = {'margin-left' : - this.container.width(), 'margin-top' : 0};
                    objTo   = {'margin-left' : 0 }
                  break;
                  case 'right':
                  case 'r':
                    objFrom = {'margin-left' : this.container.width(), 'margin-top' : 0};
                    objTo   = {'margin-left' : 0 }
                  break;
                  case 'top':
                  case 't':
                    objFrom = {'margin-top' : - this.container.height(), 'margin-left' : 0};
                    objTo   = {'margin-top' : 0 }
                  break;
                  case 'bottom':
                  case 'b':
                    objFrom = {'margin-top' : this.container.height(), 'margin-left' : 0};
                    objTo   = {'margin-top' : 0 }
                  break;
                  case 'left-fade':
                  case 'lf':
                    objFrom = {'margin-left' : -fadeMargin, 'opacity' : 0, 'margin-top' : 0};
                    objTo   = {'margin-left' : 0, 'opacity' : 1 }
                  break;
                  case 'right-fade':
                  case 'rf':
                    objFrom = {'margin-left' : fadeMargin, 'opacity' : 0, 'margin-top' : 0};
                    objTo   = {'margin-left' : 0, 'opacity' : 1 }
                  break;
                  case 'top-fade':
                  case 'tf':
                    objFrom = {'margin-top' : -fadeMargin, 'opacity' : 0, 'margin-left': 0 };
                    objTo   = {'margin-top' : 0, 'opacity' : 1 }
                  break;
                  case 'bottom-fade':
                  case 'bf':
                    objFrom = {'margin-top' : fadeMargin, 'opacity' : 0, 'margin-left': 0};
                    objTo   = {'margin-top' : 0, 'opacity' : 1 }
                  break;
                  default: // fade by default
                    justFade = true;
                  break;
              }

              if ( justFade ) {
                el.css('margin', 0)
                  .hide()
                  .fadeTo(parseInt(el.slideIn.during), 1)
              }
              else {
                el.css(objFrom) // positionate and animate
                  .show()
                  .animate(objTo, {
                    duration: parseInt(el.slideIn.during),
                    easeing:  el.slideIn.use
                });
              }
            }
            return {from : objFrom, to : objTo}
        },

        /* *************************************
         * ANIMATE TO DIRECTION
         * *************************************/
        to: function(el) {
            var objTo, objFrom,
              justFade = false,
              self   = this,
              effect;

            effect = this.carouselInvert() ?
            el.slideIn.from :
            el.slideOut.to;

            if ($.support.css3feature) {

              el.queue( function() {
                  $(this)
                    .clearState('in')
                    .addClass('out')
                    .data('activeClass', effect)
                    .addClass(effect)
                    .prepareEffect(el.slideOut.during, self.cssEasing[el.slideOut.use])

                    .dequeue();
              })
              //el.delay(50)
              el.queue( function() {
                  this.offsetWidth // reflow
                  $(this)
                    .addClass('live')
                    .dequeue();
              });
              el.delay(parseInt(el.slideOut.during)-100)

            }
            else {

              switch(effect) {
                  case 'left':
                  case 'l':
                    objFrom  = {'margin-left' : 0};
                    objTo   = {'margin-left' : - this.container.width()};
                  break;
                  case 'right':
                  case 'r':
                    objFrom  = {'margin-left' : 0};
                    objTo   = {'margin-left' : this.container.width()};
                  break;
                  case 'top':
                  case 't':
                    objFrom  = {'margin-top' : 0};
                    objTo   = {'margin-top' : -this.container.height()};
                  break;
                  case 'bottom':
                  case 'b':
                    objFrom  = {'margin-top' : 0};
                    objTo   = {'margin-top' : this.container.height()};
                  break;
                  case 'left-fade':
                  case 'lf':
                    objTo = {'margin-left' : -fadeMargin, 'opacity' : 0};
                    objFrom = {'margin-left' : 0, 'opacity' : 1 }
                  break;
                  case 'right-fade':
                  case 'rf':
                    objTo = {'margin-left' : fadeMargin, 'opacity' : 0};
                    objFrom = {'margin-left' : 0, 'opacity' : 1 }
                  break;
                  case 'top-fade':
                  case 'tf':
                    objTo = {'margin-top' : -fadeMargin, 'opacity' : 0};
                    objFrom = {'margin-top' : 0, 'opacity' : 1 }
                  break;
                  case 'bottom-fade':
                  case 'bf':
                    objTo = {'margin-top' : fadeMargin, 'opacity' : 0};
                    objFrom = {'margin-top' : 0, 'opacity' : 1 }
                  break;
                  default:
                    justFade = true;
                  break;
              }
              if ( justFade ) {
                el.fadeOut(parseInt(el.slideOut.during));
              }
              else {
                el
                  .animate(objTo, {
                    duration: parseInt(el.slideOut.during),
                    easing:   el.slideOut.use
                });
              }
            }
            return { to: objTo }
        },

        runHook: function(name, ctx, params) {
          ctx = ctx || this.container;
          params = params || [];
          this.options['_'+name] &&
            this.options['_'+name].apply(ctx, params);
          this.options[name] &&
            this.options[name].apply(ctx, params);
        }

    };


/*===================================================
  LUSH SLIDER MODE
  ===================================================*/


    function Slider( element, option ) {

      this.container = $(element);
      this.items     = this.container.children('li, .lush');

      this.itemCount = this.items.length;
      this.loopCount = 0;


      this.options   = option.slider;
      this.lush      = option;

      if(this.options.startAt < 0 || this.options.startAt >= this.itemCount)
        this.options.startAt = 0;

      // flag for slider mode
      this.lush.isSlider = true;

      // attempt to set height before start
      this.container.height(
        this.container.width() / (this.lush.baseWidth / this.lush.baseHeight)
        );

      this.sliding = false;

      // allows to set manual in slider properties
      this.options.manual = this.options.manual || this.lush.manual;

      // if manual slider, remove pauseOnHover
      if ( this.options.manual )
        this.options.pauseOnHover = false;

      // transfer deadtime to lush
      if(this.options.deadtime > 0)
        this.lush.deadtime = this.options.deadtime;

      // add a preloader
      this.preloader();

      this.prepareVideos($.proxy(function() {

        this.preload($.proxy(this.init, this));

      }, this));


    }

    Slider.prototype = {

      init: function() {
        var slideNext, slidePrev,
            initCounter = 0,
            that = this;

        // init content when all slides are ready
        this.items.one('lushInit', function() {
          if( ++ initCounter == that.itemCount) {
            that.addstuff();
            that.activePage(1);
            that.container.trigger('sliderInit');
          }
        });

        // start asap the first slide
        this.items.eq(this.options.startAt).one('lushInit', function() {
                $(this).lush('start');
                that.preloader(true);
            });

        this.items.each($.proxy(function(i, el) {

            $(el).data('slide-index', i + 1);

            slideNext = i + 1;
            slidePrev = i - 1;

            if ( i == (this.itemCount - 1) )
                slideNext = 0;
            if ( i == 0 )
                slidePrev = (this.itemCount - 1);

            $(el)
              .width( this.container.width() )
              .lush( $.extend(this.lush, {
                  autostart:  false
                , slider:     true
                , flexslider: false
                , carousel:  (!!this.options.carousel)
                , syncNext:  this.items[slideNext]
                , syncPrev:  this.items[slidePrev]
                , _onSlide:   function() {

                    that.activePage(this.data('slide-index'));

                    // check for manual stop
                    if(that.options.manual) {
                      this.lush('pause');
                    }
                    else {
                      // loops disable on manual mode
                      if( that.loopEnds.call(that) ) {
                        this.lush('pause');
                        // remove pause on hover and trigger event
                        that.container.off('.lushhover').trigger('sliderLoopEnd');
                      }
                    }
                  }
                , _onSlideIn: function() {
                    // remove running state to allow manual advance
                    if( that.options.manual ) {
                      this.removeClass('running');
                    }
                  }
                , _onSlided: function() {

                    // reset video
                    this.children('.lush-video-wrapper').each(function() {
                      that.resetVideo($(this));
                    });

                  }
                , _onItemSlideIn: function() {
                    // when every item slides in screen, check for video autoplay
                    if( that.options.videoAutoplay ) {
                      if( this.hasClass('lush-video-wrapper') ) {
                        this.click();
                      }
                    }
                }
              }))
          }, this));

      },

      preloader: function(remove) {
          if(remove) {
            this.container
              .children('.lush-preloader')
              .remove();
          }
          else {
            this.container
                .append($('<div/>', {
                        "class" : 'lush-preloader'
                }));
          }
      },

      prepareVideos: function(callback) {

        var that = this,
            videos = [],
            videoLen = 0,
            videoCnt = 0;

        // Collect all Vimeo videos
        this.items.find('iframe[src*="player.vimeo"]').each(function() {

          videoLen = videos.push({
            iframe: $(this),
            type:   'vm'
          });

        })
        // Collect all Youtube videos
        this.items.find('iframe[src*="www.youtu"]').each(function() {

          videoLen = videos.push({
            iframe: $(this),
            type:   'yt'
          });

        })

        if(videoLen == 0) {
          callback();
          return;
        }

        for(var i = 0; i < videoLen; i++) {

          var videoIframe  = videos[i].iframe,
              videoWrapper = wrapIframe(videoIframe);

          videoWrapper.on('click', initVideo);

          !function(wrpr, ifr) {

            switch(videos[i].type) {
              case 'yt':
                var ytId = ifr.data('LushVideosrc').split('embed/')[1].split('?')[0];
                $.getJSON(that.options.ytServerApiUrl + '?vid='+ ytId, function(data) {

                  addPreview(wrpr, data['thumbnail']['maxresDefault']);

                  ifr.data('LushVideoduration', parseInt(data['duration_sec']) * 1000 );

                  checkAllDone();
                })

              break;
              case 'vm':
                var vmId = ifr.data('LushVideosrc').split('video/')[1].split('?')[0];
                $.getJSON('http://vimeo.com/api/v2/video/' + vmId +'.json?callback=\?', function(data){

                  addPreview(wrpr, data[0]['thumbnail_large'])

                  ifr.data('LushVideoduration', parseInt( data[0]['duration'] ) * 1000);

                  checkAllDone();

                })

              break;
            }

          }(videoWrapper, videoIframe);

        }

        // helper: run callback when all video request are done
        function checkAllDone() {
          if(++videoCnt == videoLen)
            callback();
        }

        // helper: add video image preview
        function addPreview(wrapper, url) {
          $('<img>')
            .appendTo( wrapper )
            .addClass('lush-video-preview')
            .attr('src', url );
        }

        // helper: wrap video iframe
        function wrapIframe(iframe) {
            var wrapper =
              iframe
                .wrap('<div class="lush-video-wrapper" />')
                .parent()
                .attr({
                  'data-slide-in':    iframe.attr('data-slide-in' ),
                  'data-slide-out':   iframe.attr('data-slide-out')
                })
                .css({
                  'width':            iframe.width(),
                  'height':           iframe.height(),
                  'top':              iframe[0].style.top,
                  'left':             iframe[0].style.left
                });
            // remove original properties
            iframe.css({
                'width':            '100%',
                'height':           '100%',
                'top':              0,
                'left':             0
            });

            iframe
              .data( 'LushVideosrc',
                     iframe.attr('src') + (iframe.attr('src').indexOf('?') == -1?'?':'&') + 'autoplay=1' )
              .attr('src','');

            return wrapper;
        }

        // helper: adds click handler to video wrapper
        function initVideo() {

            var $this = $(this),
                iframe = $this.children('iframe');

            if( that.options.pauseOnVideo )
              that.pauseSlider();

            iframe.one('load', function() {

              $this.addClass('playing')

              $this.children('.lush-video-preview')
                   .delay(that.options.videoAutoplayDelay)
                   .fadeOut(that.options.videoPreviewFadeOut, function() {

                        var videotimer = setTimeout(function() {

                            iframe.data( 'LushVideotimer', '' );
                            that.resetVideo($this, function() {

                              if( that.options.videoAutoresume)
                                that.resumeSlider();

                            });

                        }, iframe.data('LushVideoduration') + that.options.videoTimerDelay);

                        iframe.data( 'LushVideotimer', videotimer );

                  });
            }).attr('src', iframe.data('LushVideosrc'));

        }

      },

      resetVideo: function(wrapper, callback) {
          var ifr = wrapper.children('iframe'),
              img = wrapper.children('.lush-video-preview');

          window.clearTimeout( ifr.data('LushVideotimer') );

          img.fadeIn(this.options.videoPreviewFadeIn, function() {
            ifr.attr('src','');
            callback && callback();
          });

          wrapper.removeClass('playing');
      },

      addstuff: function() {

          /* Create navigation items */
          if(this.options.navigation)
            this.addnav();

          /* Create shadow container */
          if(this.options.shadow)
            $('<div/>', {
              'class': classShadow
            }).appendTo(this.container);

          this.addevents();

          this.updateNav();
      },

      preload: function(callback) {

          var src = false,
              bg = this.container.css('background-image');

          if( bg && bg !== 'none' && bg.indexOf('url') >= 0 )
            src = bg.match(/url\((.*)\)/)[1].replace(/"/gi, '');

          if ( ! src )
              callback();
          else
              $('<img>').load(callback).attr('src', src);

      },


      addnav: function() {
        var that = this;

        this.nav = $('<div/>').appendTo(this.container).addClass(classNav);

        $('<a href="#" class="'+classPrev+'">&lt;</a>').appendTo(this.nav)

        if(this.options.pager) {
              for (i=0; i < this.itemCount; i++){
          $('<a href="#" class="'+classPage+'" rel="'+(i+1)+'">'+(i+1)+'</a>').appendTo(this.nav)
              }
        }

        $('<a href="#" class="'+classNext+'">&gt;</a>').appendTo(this.nav);

      },

      updateNav: function() {
        var lh = this.nav && parseInt(this.nav.css('line-height'));

        if(this.nav) {
          lh = lh === 0 ? 0 : this.container.height() /2
          this.nav.css({
            left: this.container.width() /2 - this.nav.width()/2,
            lineHeight: lh + 'px'
          })
          // fix ie7
          if (navigator.appVersion.indexOf("MSIE 7.") != -1)
            this.nav.find('.lush-page').each(function() {
              $(this).css('margin-top',
                lh === 0 ? 0 : (lh - $(this).height()) + 'px')
            })
        }
      },

      activePage: function(index) {
          if ( this.nav ) {
            this.nav.children('.current').removeClass('current')
            this.nav.children('a[rel=' + index + ']').addClass('current')
          }
      },

      pauseSlider: function(){

        this.items.lush('pause');

      },

      resumeSlider: function(){

        if( this.items.filter('.active').find('.playing').length == 0)
          this.items.lush('resume');
      },

      addevents: function() {
        var that = this,
            advanceNext  = function(){ that.items.filter('.active').lush('next'); },
            advancePrev  = function(){ that.items.filter('.active').lush('prev'); };

        //-- Responsive Events
        if(this.options.responsive) {

          $(window).resize(function() {

            that.items.each(function(i, el) {
              $(el).width(that.container.width())
            });

            setTimeout($.proxy(that.updateNav,that),100);
          });

        }

        //-- Navigation control Events
        if(this.options.navigation) {
          this.nav.on('click.lush', function(event) {
            event.preventDefault();
            var $target = $(event.target);

            if(that.sliding) return;
            if( $target.is('.'+classPrev) ) advancePrev();
            if( $target.is('.'+classNext) ) advanceNext();
            if( $target.is('.'+classPage) ) that.slideto.call(that, parseInt($target.attr('rel')) )
            return false;
          })
        }

        //-- Extra Navigation control Events
        $('.'+classExternal).on('click.lush',function(e){

          var target = parseInt($(this).data('slideto'))
          that.slideto(target);

        })

        //-- Mouse pauseOnHover Event
        if(this.options.pauseOnHover) {

            this.container
              .on('mouseenter.lushhover.in',
                  $.proxy(this.pauseSlider,that))
              .on('mouseleave.lushhover.out',
                  $.proxy(this.resumeSlider,that));

        }

        //-- Keyboard control Events
        if(this.options.keyboard)
          $(document).on('keyup.lush',   function(event) {
            var keycode = event.keyCode;
            if(that.sliding) return;
            if(keycode == 37) advancePrev();
            if(keycode == 39) advanceNext();
          });

        //-- Touch Navigation Events
        if( ('ontouchstart' in window) && this.options.touch ) {

          // prepare to store touch event data
          this.touchData = {};

          this.container.on('touchstart', function(event) {
            var t = event.touches ? event.touches : event.originalEvent.touches;
            if( t.length == 1 )
              that.touchData.touchStartX = that.touchData.touchEndX = t[0].clientX;
          });

          this.container.on('touchmove', function(event) {
            var t = event.touches ? event.touches : event.originalEvent.touches;
            if( t.length == 1 )
              that.touchData.touchEndX = t[0].clientX;
            if( Math.abs( that.touchData.touchStartX - that.touchData.touchEndX ) > 45 )
                event.preventDefault();
          });

          this.container.on('touchend', function(event) {
            if( Math.abs( that.touchData.touchStartX - that.touchData.touchEndX ) > 45 )
            {
              if( that.touchData.touchStartX - that.touchData.touchEndX > 0 )
                advanceNext();
              else
                advancePrev();
            }
          });
        }
      },

      loopEnds: function() {
        this.container.trigger('sliderLoop', [this.loopCount]);
        return ( this.options.loop && (this.options.loop * this.itemCount) <= (this.loopCount++) );
      },

      slideto: function(target) {

        var that      = this,
            current   = this.items.filter('.active'),
            isRunning = current.hasClass('running'),
            action    = 'stop', //this.lush.manual ? 'slideout' : 'stop',
            nextSlide;

        // manual: disable advance until animation ends
        if(this.options.lockOnManual && this.options.manual && isRunning)
            return;

        if( !this.sliding && (target > 0 && target <= this.itemCount)) {

          this.sliding = true;

          nextSlide = this.items.eq(target - 1);

          if(nextSlide.hasClass('active')) {
            this.sliding = false;
            return;
          }

          /* When current ends, start next slide */
          current.data('lush').state('resume').stop();

          setTimeout(function() {

            nextSlide.one('slideStart',
              function() {

                  that.sliding = false;

            }).lush('start');

          }, that.options.delayed)

        } // if not sliding
      }

    } /* end Slider proptotype */


/*===================================================
  LUSH FLEXSLIDER MODE
  ===================================================*/


    function goFlexslider( options ) {

      var   sel          = $(this)
          , fsOptions    = $.extend({}, $.flexslider.defaults, options.flexslider)
          , items        = sel.find(fsOptions.selector)
          , count        = items.length
          , fsNamespace  = fsOptions.namespace ? fsOptions.namespace : 'flex-'
          , fsActive     = fsNamespace + 'active-slide'
          , fsNext       = fsNamespace + 'next'
          , fsPrev       = fsNamespace + 'prev'
          , paused       = false
          , pauseSlider  = function(){ items.lush('pause'); }
          , resumeSlider = function(){ items.lush('resume'); }
          , restOfSlide
          ;



      // hide all items so FS can calcualte correct size
      items.each(function(i, el){
        $(el).children().not('.ignore').hide()
      })

      sel.flexslider($.extend(fsOptions, {
          start : function(slider) {
                slider.slides.eq(0).one('lushInit', function(){
                  $(this).lush('start');
                });

                slider.slides.lush($.extend(options, {
                      autostart: false,
                      slider: false,
                      onSlided: goNextSlide
                    }));
            },
            after : function(slider) {
                slider.slides.filter('.'+fsActive).lush('start');
            },
            before : function(slider) {
                restOfSlide = slider.slides.not(':eq('+slider.animatingTo+')').lush('stop');
            }
        }));

      // make flexslider advance to next slide
      function goNextSlide() {

            // no autoslide on manual advance
            if ( ! sel.data('flexslider').animating && !paused)
                sel.flexslider("next");

            return true;
      }

      // 1.2: Added pauseonhover for flexslider mode
      if(options.flexslider.pauseOnHover){
          sel.hover( function() {
            paused = true;
            pauseSlider();
          },function() {
            paused = false;
            resumeSlider();
            if(!sel.find('.running').length)
              goNextSlide();
          })
      }

  } //goFlexslider



/*===================================================
  PLUGIN INITIALIZATION
  ===================================================*/

    $.fn[pluginName] = function ( option ) {

        if ((typeof option).match("object|undefined")) {

            return this.each(function () {

                var $this = $(this),
                    settings = $.extend(true, {},
                                    $.fn[pluginName].defaults,
                                    typeof option == 'object' && option,
                                    getLushData(this));

                if ( $this.hasClass(sliderClass) ) {

                  if( ! $.data(this, sliderData) )
                      $.data(this, sliderData, new Slider(this, settings));

                }
                else if ( $this.hasClass(flexsliderClass) ) {

                  if(!$.data(this, flexsliderData) && $.flexslider) {
          					$.data(this, flexsliderData, 1);
          					goFlexslider.call(this, settings);
                  }
                }
                else {

                  if ( ! $.data(this, pluginName) ) {
                      new Lush( this, settings )
                  }
                }
            });
        }
        else {
            return this.each(function (t) {

                // API Commands
                if (typeof option == "string") {

                    var obj = $.data(this, pluginName);

                    if ( ! obj ) return;


                    switch (option) {
                        case 'start' :
                        case 'stop'  :
                        case 'resize':   obj[option]();         break;
                        case 'prev'  :
                        case 'next'  :   obj.go(option);        break;
                        case 'pause' :
                        case 'resume':   obj.state(option);     break;
                    }

                }
                // API command move to N Slide
                if (typeof option == "number") {
                  var slider = $.data(this, sliderData);
                  slider.slideto(option)
                }

            });
        }

        // since jquery parses all data attribute
        // this need custom detection and treatment
        function getLushData(node){
          var d = { slider: {} },
              re_dataAttr = /^data\-(.+)$/;

          $.each(node.attributes, function(index, attr) {
              if (re_dataAttr.test(attr.nodeName)) {
                  var parts = attr.nodeName.split('-'),
                      type = parts[1],
                      key = $.camelCase(parts.slice( type == 'slider' ? 2 : 1 ).join('-'));

                  if(type == 'slider')
                    d.slider[key] = dataType(attr.nodeValue);
                  else
                    d[key] = dataType(attr.nodeValue);
              }
          });
          return d;
        }

        function dataType(data) {
          return data === "true" ? true :
                 data === "false" ? false :
                 data === "null" ? null :
                 jQuery.isNumeric( data ) ? parseFloat( data ) : data;
        }
    };


/*===================================================
  PLUGIN AUTOSTART
  ===================================================*/
    $(function() {

      $(".lush-slider.autoload, .lush.autoload").lush();

    })

/*===================================================
  PLUGIN DEFAULTS
  ===================================================*/

  $.fn[pluginName].defaults = {

          // ANIMATION PARAMS
          param : {
                at:     0
              , from:   'left'
              , to:     'right'
              , use:    'swing'
              , during: 1000
              , plus:   0
              , force:  false
          }

          // PLUGIN OPTIONS
          , autostart:  true      // auto start plugin
          , baseWidth:  1140      // orignal slide widht
          , baseHeight: 450       // and original slide height (ratio ~2.5)
          , direction:  'next'    // or "prev" (next==right/prev==left)
          , manual:     false     // manual advance mode
          , slider:     false     // slider mode detection (internal)
          , flexslider: false     // flexslider options object
          , syncNext:   ''        // next selector (internal)
          , syncPrev:   ''        // prev selector (internal)

          // SLIDER OPTIONS
          , slider : {
                pauseOnHover:         false    // pause slider on mouse hover
              , pauseOnVideo:         true     // pause slider when playing a video
              , navigation:           true     // show navigation controls?
              , pager:                true     // show pager controls?
              , shadow:               true     // show slider shadow element?
              , keyboard:             true     // allow keyboard navigation?
              , touch:                true     // allow touch swipe gestures for navigation?
              , responsive:           true     // enable responsive mode?
              , loop:                 0        // how many times loop through all slides?
              , carousel:             false    // carousel mode? inverts animations when direction changes
              , deadtime:             0        // extra deadtime in ms between animation in/out
              , videoAutoplay:        false    // allows to play videos automatically
              , videoAutoresume:      true     // resume slideshow after video playback ends
              , videoAutoplayDelay:   500      // a delay before send play to video
              , videoPreviewFadeOut:  700      // fadeout time for preview image
              , videoPreviewFadeIn:   400      // fadein time for preview image
              , videoTimerDelay:      1000     // increments the time to wait the video ends its playback
              , delayed:              250      // ms to delay before advance (internal)
              , lockOnManual:         true     // disable advance when animation is running on manual mode
              , startAt:              0        // Slide index to start from (zero based).
              , ytServerApiUrl:       ''       // server url of custom youtube API
          }

          // CALLBACKS
          , onInit:          function() {}    // once the plugin is initialized (preloaded)
          , onSlide:         function() {}    // when the current slide starts
          , onSlideIn:       function() {}    // when all slide element are in screen
          , onSlideOut:      function() {}    // when all slide element are out screen
          , onSlided:        function() {}    // when the current slide ends
          , onItemSlideIn:   function() {}    // for every slide element when is in screen
          , onItemSlideOut:  function() {}    // for every slide element when is out screen
      };



})( jQuery, window, document );
