module.exports = function(grunt) {
    require('jit-grunt')(grunt, {
        sprite: 'grunt-spritesmith',
        processhtml: 'grunt-processhtml'
    });
    var base_dir = 'bookelgouna/common/static/';
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        less: {
            development: {
                options: {
                    compress: true,
                    optimization: 2
                },
                files: {
                    "css/style.css": "css/style.less" // destination file and source file
                }
            }
        },

        concat: {
             dist: {
                src: [
                    'js/lib/jquery-1.11.2.js',
                    'js/lib/css3-mediaqueries.js',
                    'js/lib/jquery-ui.js',
                    'js/lib/jquery.nouislider.all.min.js',
                    'js/lib/owl.carousel.js',
                    'js/lib/placeholders.min.js',
                    'js/lib/select2.js',
                    'js/lib/jquery.raty.js',
                    'js/lib/jquery.history.js',
                    'js/lib/jquery.form.js',
                    'js/lib/jquery.noty.packaged.min.js',
                    'js/lib/jquery.ellipsis.min.js',
                    // 'js/lib/jquery.dataTables.min.js',
                    // 'js/lib/jquery.jscrollpane.min.js',
                    // 'js/lib/jquery.mousewheel.js',
                    // 'js/lib/mwheelIntent.js',
                    'js/lib/handlebars-v3.0.0.js',
                    'js/lib/jquery.visible.js',
                    'js/lib/jquery.magnific-popup.min.js',
                    'js/lib/jquery-ui-timepicker-addon.js',
                    'js/lib/jquery.nicescroll.min.js',
                    'js/lib/bootstrap-progressbar.js',
                    'js/lib/purl.min.js'
                ],
                dest: 'js/lib.js',
            },
            css: {
                src: [
                    'css/style.css',
                    'css/sprites.css',
                    'css/plugins/*.css' //For owl slider

                ],
                dest: 'css/result.css'
            }
        },
        uglify: {
            deps: {
                files: {
                    'js/lib.min.js': ['js/lib.js']
                }
            },
            script: {
                files: {
                    'js/script.min.js': ['js/script.js']
                }
            }
        },
        processhtml: {
            dev: {
                files: {
                    '../../templates/base_site.html': ['../../templates/base_site.html']
                }
            },
            prod: {
                files: {
                    '../../templates/base_site.html': ['../../templates/base_site.html']
                }
            }
        },
        sprite:{
            options: {
                livereload: true,
                total_height: 100,
            },
            icons: {
                src: 'images/sprite-icon/*.png',
                dest: 'images/spritesheet-icons.png',
                destCss: 'css/sprites.css',
                padding: 2,
                algorithm: 'binary-tree'
            },
            backs: {
                src: 'images/sprite-back/*.png',
                dest: 'images/spritesheet-backs.png',
                destCss: 'css/sprites-back.css',
                padding: 2,
                algorithm: 'top-down',
                algorithmOpts: {
                    sort: false
                }
            },
            menu: {
                src: 'images/sprite-menu-ic/*.png',
                dest: 'images/spritesheet-menu-ic.png',
                destCss: 'css/sprites-backs2.css',
                padding: 2,
                algorithm: 'top-down',
                algorithmOpts: {
                    sort: false
                }
            }
        },
        watch: {
            scripts: {
                files: ['../../../Gruntfile.js', 'js/script.js'],
                tasks: ['default'],
                options: {
                    spawn: false
                }
            },
            less: {
                files: ['css/*.less'],
                tasks: ['less', 'concat:css'],
                options: {
                    spawn: false
                }
            }
        }       
    });

//   Explicit tasks loading is not required because of jit-grunt usage https://github.com/shootaroo/jit-grunt
    grunt.file.setBase(base_dir);
    grunt.registerTask('deploy', ['less', 'sprite', 'concat', 'uglify', 'processhtml:prod']);
    grunt.registerTask('default', ['less', 'sprite', 'concat', 'processhtml:dev', 'watch']);

};
