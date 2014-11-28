var autoprefixer = require('gulp-autoprefixer'),
    changed = require('gulp-changed'),
    concat = require('gulp-concat'),
    base64 = require('gulp-base64'),
    filter = require('gulp-filter'),
    gulp = require('gulp'),
    gutil = require('gulp-util'),
    minifyCSS = require('gulp-minify-css'),
    spritesmith = require('gulp.spritesmith'),
    watch = require('gulp-watch');

var _ = require("underscore"),
    browserSync = require('browser-sync'),
    fs = require('fs'),
    glob = require("glob"),
    minimatch = require("minimatch");

PROJECT_APPS_PATH = './pyramid_sacrud_example/includes/';
PROJECT_MODULES_PATH = '../*/';
PROJECT_STATIC_PATH = '';

function addWatchFolders(appName, type) {
    if(!type) gutil.log(gutil.colors.red('Failed addWatchFolders "type" undefined'));
    var modules = _.filter(glob.sync(PROJECT_MODULES_PATH), function(folder){
        moduleName = folder.match(/.+\/(.+)\/$/)[1];
        return moduleName.indexOf(appName) > -1;
    });
    var modulePath = _.first(modules);
    if (type === 'css') {
        if (modulePath !== undefined) path = modulePath + appName + '/static/' + appName + '/css/**/*.css';
        else path = PROJECT_APPS_PATH + appName + '/static/' + appName + '/css/**/*.css' ;
    }
    if (type === 'img') {
        if (modulePath !== undefined) path = modulePath + appName + '/static/' + appName + '/img/**/*';
        else path = PROJECT_APPS_PATH + appName + '/static/' + appName + '/img/**/*' ;
    }
    if (type === 'templates') {
        if (modulePath !== undefined) path = modulePath + appName + '/templates/**/*';
        else path = PROJECT_APPS_PATH + appName + appName + '/templates/**/*';
    }
    return path;
}

function getFiles(path, type) {
    if(!path) gutil.log(gutil.colors.red('Failed getFiles "path" undefined'));
    if(!type) gutil.log(gutil.colors.red('Failed getFiles "type" undefined'));
    var files = glob.sync(path + '**/*.*'),
        target = minimatch.match(files, '__*.*', { matchBase: true }),
        ignore = _.map(target, function(item){ return '!' + item; }),
        result = files.concat(ignore);
    return result;
}

function getFileName(file) {
    return file.split('/').pop();
}

function getConcatFiles(appName, type) {

    if(!type) gutil.log(gutil.colors.red('Failed getConcatFiles "folder" undefined'));
    var redefineModuleFiles = [];

    /* Django Path */
    var targetPrefix = appName + '/static/' + appName + '/',
        targetPath = PROJECT_APPS_PATH + targetPrefix + type + '/';

    /* Pyramid Path */
    if (fs.existsSync(targetPath) === false) {
        targetPrefix = appName + '/static/';
        targetPath = PROJECT_APPS_PATH + targetPrefix + type + '/';
    }


    projectAppFiles = getFiles(targetPath, type);
    if (type === 'templates') projectAppFiles = getFiles(PROJECT_APPS_PATH + appName + '/templates/', type);
    if (appName === 'static') {
        projectAppFiles = getFiles(PROJECT_STATIC_PATH + type + '/', type);
        if (type === 'templates') projectAppFiles = getFiles('./templates/', type);
    }

    /* Find Redifine Modules */
    redefineModules = _.filter(glob.sync(PROJECT_MODULES_PATH), function(folder){
        redefineModuleName = folder.match(/.+\/(.+)\/$/)[1];
        return redefineModuleName.indexOf(appName) > -1;
    });

    redefineModulePath = _.first(redefineModules);

    if (redefineModulePath !== undefined) {
        /* Redefine Path Django */
        var path = redefineModulePath + appName + '/static/' + appName + '/' + type + '/';
        /* Redefine Path Pyramid */
        if (fs.existsSync(path) === false) path = redefineModulePath + redefineModulePath.substring(3) + 'static/' + type + '/';
        if (type === 'templates') path = redefineModulePath + appName + '/templates/';

        redefineModuleFiles = _.map(getFiles(path, type), function (item) {
            var redefineFile = getFileName(item);
            projectAppFiles.forEach(function (include_item) {
                var projectFile = getFileName(include_item);
                if (item.indexOf('!') === 0) return item;
                if (redefineFile === projectFile) item = '!' + item;
            });
            return item;
        });
    }

    var concatFiles = redefineModuleFiles.concat(projectAppFiles);
    concatFiles = _.sortBy(concatFiles, function (item) { return item.indexOf('!') === 0; });
    concatFiles = _.uniq(concatFiles);
    return concatFiles;
}

function getExistConcatFile(appName, type) {

    var target = null,
        targetPrefix = appName + '/static/' + appName + '/',
        targetPath = PROJECT_APPS_PATH + targetPrefix + type + '/';

    if (fs.existsSync(targetPath) === false) {
        targetPrefix = appName + '/static/';
        targetPath = PROJECT_APPS_PATH + targetPrefix + type + '/';
    }

    var files = getFiles(targetPath, type);

    if (appName === 'static') files = getFiles(PROJECT_STATIC_PATH + type, type);

    /* Find Not Redefined Modules */
    if (files.length <= 0) {
        modules = _.filter(glob.sync(PROJECT_MODULES_PATH), function(folder){
            moduleName = folder.match(/.+\/(.+)\/$/)[1];
            return moduleName.indexOf(appName) > -1;
        });
        modulePath = _.first(modules);
        if (modulePath !== undefined) target = modulePath + targetPrefix + type + '/';
        else target = PROJECT_APPS_PATH + targetPrefix + type + '/';
    } else {
        target = PROJECT_APPS_PATH + targetPrefix + type + '/';
        if (appName === 'static') target = PROJECT_STATIC_PATH + type + '/';
    }
    return target;
}

gulp.task('browser-sync', function() {
    browserSync({
        proxy: "localhost:8000",
    });
});

gulp.task('css', function() {
    var appList = glob.sync(PROJECT_APPS_PATH + '*/'),
        type = 'css';
    if (fs.existsSync(PROJECT_STATIC_PATH)) appList.push(PROJECT_STATIC_PATH);
    appList.forEach(function(folder) {
        appName = folder.match(/.+\/(.+)\/$/)[1];
        gulp.src(getConcatFiles(appName, type))
            .pipe(filter('*.css'))
            .pipe(autoprefixer({
                browsers: ['Firefox >= 3', 'Explorer >= 6', 'Opera >= 9', 'Chrome >= 15', 'Safari >= 4', '> 1%'],
                cascade: false
            }))
            .pipe(base64({
                extensions: ['png', 'jpg', 'gif'],
                maxImageSize: 8 * 4096
            }))
            .pipe(minifyCSS())
            .pipe(concat('__' + appName + '.css'))
            .pipe(gulp.dest(getExistConcatFile(appName, type)))
            .pipe(browserSync.reload({ stream:true }));
        gutil.log(gutil.colors.green('Create file: ' + getExistConcatFile(appName, type) + '__' + appName + '.css'));
    });
});

gulp.task('img', function () {
    var appList = glob.sync(PROJECT_APPS_PATH + '*/'),
        type = 'img';
    if (fs.existsSync(PROJECT_STATIC_PATH)) appList.push(PROJECT_STATIC_PATH);
    appList.forEach(function(folder) {
        appName = folder.match(/.+\/(.+)\/$/)[1];
        appFiles = getConcatFiles(appName, type);
        if (appFiles.length !== 0) {
            sprite = gulp.src(appFiles)
                .pipe(filter(['*.png', '*.jpg', '*.gif', '!*-sprite.png']))
                .pipe(spritesmith({
                    imgName: appName + '-sprite.png',
                    imgPath: '../img/' + appName + '-sprite.png',
                    cssName: appName +'-sprite.css',
                    algorithm: 'binary-tree',
                    source_image: 'asdasdasdasd',
                    cssOpts: {
                        cssClass: function (item) {
                            return '.' + item.name;
                        }
                    }
                }));
            sprite.img.pipe(gulp.dest(getExistConcatFile(appName, type)));

            var path = getExistConcatFile(appName, type);
            path = path.substr(0, path.length - 4) + 'css/';

            sprite.css.pipe(gulp.dest(path));
        }
    });
});

gulp.task('templates', function() {
    var appList = glob.sync(PROJECT_APPS_PATH + '*/'),
        type = 'templates';
    if (fs.existsSync(PROJECT_STATIC_PATH)) appList.push(PROJECT_STATIC_PATH);
    appList.forEach(function(folder) {
        appName = folder.match(/.+\/(.+)\/$/)[1];
        gulp.src(getConcatFiles(appName, type))
            .pipe(browserSync.reload({ stream:true }));
    });
});



gulp.task('watch', function () {

    var types = ['templates', 'css'],
        watchFiles = [];

    types.forEach(function(type) {
        var appList = glob.sync(PROJECT_APPS_PATH + '*/');
        if (fs.existsSync(PROJECT_STATIC_PATH)) appList.push(PROJECT_STATIC_PATH);
        appList.forEach(function(folder) {
            appName = folder.match(/.+\/(.+)\/$/)[1];
            watchFiles = watchFiles.concat(getConcatFiles(appName, type));
            watchFiles.push(addWatchFolders(appName, type));
        });
        watchFiles = _.sortBy(watchFiles, function(item){ if (item.indexOf('!') !== 0) return item; });

        watch(watchFiles, function (files, cb) {
            gulp.start(type, cb);
            gutil.log(gutil.colors.yellow('Waiting...'));
        });

    });
});

gulp.task('default', ['watch', 'browser-sync']);