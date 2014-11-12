var gulp = require('gulp'),
    autoprefixer = require('gulp-autoprefixer'),
    concat = require('gulp-concat'),
    watch = require('gulp-watch'),
    browserSync = require('browser-sync');

var staticPath = '../pyramid_sacrud_example/includes/home/static/';
var templatePath = '../pyramid_sacrud_example/includes/';
var cssFiles = [staticPath + 'css/*.css', staticPath + 'css/**/*.css', '!' + staticPath + 'css/__main.css'];
var templates = [templatePath + '*.jinja2', templatePath + '**/*.jinja2'];
var jsFiles = [staticPath + 'js/*.js', staticPath + 'js/**/*.js', '!' + staticPath + 'js/__main.js'];

gulp.task('browser-sync', function() {
    browserSync({
        proxy: "localhost:8000",
    });
});

gulp.task('css', function() {
    gulp.src(cssFiles)
        .pipe(autoprefixer({
            browsers: [
                'Firefox >= 3',
                'Explorer >= 6',
                'Opera >= 9',
                'Chrome >= 15',
                'Safari >= 4',
                '> 1%'],
            cascade: false
        }))
        .pipe(concat('__main.css'))
        .pipe(gulp.dest(staticPath + 'css/'))
        .pipe(browserSync.reload({stream:true}));
});


gulp.task('js', function() {
    gulp.src(jsFiles)
        .pipe(concat('__main.js'))
        .pipe(gulp.dest(staticPath + 'js/'));
});



gulp.task('templates', function() {
    gulp.src(templates)
        .pipe(browserSync.reload({stream:true}));
});



gulp.task('watch', ['browser-sync'], function () {
    watch(cssFiles, function (files) {
        return gulp.start('css');
    });
    watch(jsFiles, function (files) {
        return gulp.start('js');
    });
});

gulp.task('default', ['browser-sync'], function () {
    gulp.watch(cssFiles, ['css', browserSync.reload]);
    gulp.watch(jsFiles, ['js', browserSync.reload]);
    gulp.watch(templates, ['templates', browserSync.reload]);});
