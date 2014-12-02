var autoprefixer = require('gulp-autoprefixer'),
    base64 = require('gulp-base64'),
    concat = require('gulp-concat'),
    imagemin = require('gulp-imagemin'),
    filter = require('gulp-filter'),
    gulp = require('gulp'),
    gutil = require('gulp-util'),
    minifyCSS = require('gulp-minify-css'),
    newer = require('gulp-newer'),
    spritesmith = require('gulp.spritesmith'),
    watch = require('gulp-watch');

var _ = require("underscore"),
    browserSync = require('browser-sync'),
    fs = require('fs'),
    glob = require("glob"),
    map = require('vinyl-map'),
    minimatch = require("minimatch"),
    pngquant = require('imagemin-pngquant');

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
        if (modulePath !== undefined) path = modulePath + appName + '/static/' + appName + '/' + type + '/**/*.css';
        else path = PROJECT_APPS_PATH + appName + '/static/' + appName + '/' + type +'/**/*.css';
    }
    if (type === 'img') {
        if (modulePath !== undefined) path = modulePath + appName + '/static/' + appName + '/' + type +'/**/*';
        else path = PROJECT_APPS_PATH + appName + '/static/' + appName + '/' + type +'/**/*' ;
    }
    if (type === 'templates') {
        if (modulePath !== undefined) path = modulePath + appName + '/' + type + '/**/*';
        else path = PROJECT_APPS_PATH + appName + appName + '/' + type + '/**/*';
    }
    return path;
}

function getFilesList(path, type) {
    if(!path) gutil.log(gutil.colors.red('Failed getFilesList "path" undefined'));
    if(!type) gutil.log(gutil.colors.red('Failed getFilesList "type" undefined'));

    var files = glob.sync(path + '**/*.*'),
        target = minimatch.match(files, '__*.*', { matchBase: true }),
        ignore = _.map(target, function(item){ return '!' + item; }),
        result = files.concat(ignore);

    return result;
}

function getFileName(file) {
    return file.split('/').pop();
}

function getPath(appName, type) {

    /* Django */
    var pathPrefix = appName + '/static/' + appName + '/',
        path = PROJECT_APPS_PATH + pathPrefix + type + '/';

    /* Pyramid */
    if (fs.existsSync(path) === false) {
        pathPrefix = appName + '/static/';
        path = PROJECT_APPS_PATH + pathPrefix + type + '/';
    }

    if (type === 'templates') path = PROJECT_APPS_PATH + appName + '/' + type + '/';

    if (appName === 'static') {
        path = PROJECT_STATIC_PATH + type + '/';
        if (type === 'templates') { path = './' + type + '/'; }
    }

    return path;
}

function getConcatFiles(appName, type) {
    if(!type) gutil.log(gutil.colors.red('Failed getConcatFiles "folder" undefined'));

    var appPath = getPath(appName, type),
        appFiles = getFilesList(appPath, type);

    /* Find Redifine Modules */
    var redefineModuleFiles = [],
        redefineModules = _.filter(glob.sync(PROJECT_MODULES_PATH), function(folder){
        redefineModuleName = folder.match(/.+\/(.+)\/$/)[1];
        return redefineModuleName.indexOf(appName) > -1;
    });

    redefineModulePath = _.first(redefineModules);

    if (redefineModulePath !== undefined) {
        /* Django Path  */
        var path = redefineModulePath + appName + '/static/' + appName + '/' + type + '/';
        /* Pyramid Path */
        if (fs.existsSync(path) === false) {
            path = redefineModulePath + redefineModulePath.substring(3) + 'static/' + type + '/';
        }

        if (type === 'templates') path = redefineModulePath + appName + '/' + type + '/';

        redefineModuleFiles = _.map(getFilesList(path, type), function (item) {
            var redefineFile = getFileName(item);
            appFiles.forEach(function (include_item) {
                var projectFile = getFileName(include_item);
                if (item.indexOf('!') === 0) return item;
                if (redefineFile === projectFile) item = '!' + item;
            });
            return item;
        });

    }

    var concatFiles = redefineModuleFiles.concat(appFiles);
    concatFiles = _.sortBy(concatFiles, function (item) { return item.indexOf('!') === 0; });
    concatFiles = _.uniq(concatFiles);

    return concatFiles;
}

function getExistingFiles(appName, type) {

    var target = getPath(appName, type),
        appPath = getPath(appName, type),
        appFiles = getFilesList(appPath, type);

    if (appFiles.length <= 0) {
        /* Template not exist search in module */
        modules = _.filter(glob.sync(PROJECT_MODULES_PATH), function(folder){
            moduleName = folder.match(/.+\/(.+)\/$/)[1];
            return moduleName.indexOf(appName) > -1;
        });
        modulePath = _.first(modules);

        if (modulePath !== undefined) {
            /* Find module path */
            target = modulePath + appName + '/static/' + appName + '/' + type + '/';
            if (fs.existsSync(target) === false) {
                target = modulePath + modulePath.substring(3) + 'static/' + type + '/';
            }
            if (type === 'templates') target = modulePath + appName + '/' + type + '/';
        }
    }
    return target;
}

gulp.task('browser-sync', function() {
    browserSync({
        proxy: "localhost:8000",
        logLevel: "silent",
        //reloadDelay: 1000,
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
            //.pipe(newer(getExistingFiles(appName, type) + '__' + appName + '.css'))
            .pipe(autoprefixer({
                browsers: ['Firefox >= 3', 'Explorer >= 6', 'Opera >= 9', 'Chrome >= 15', 'Safari >= 4', '> 1%'],
                cascade: false
            }))
            .on('error', function(err) {
                gutil.log(gutil.colors.red('Failed to autoprefixer'), gutil.colors.yellow(err.message));
            })
            .pipe(base64({
                extensions: ['png', 'jpg', 'gif'],
                maxImageSize: 8 * 4096
            }))
            .on('error', gutil.log)
            .pipe(minifyCSS())
            .pipe(map(function(code, filename) { gutil.log('Use ' + gutil.colors.yellow(filename)); }))
            .pipe(concat('__' + appName + '.css'))
            .pipe(gulp.dest(getExistingFiles(appName, type)))
            .pipe(map(function(code, filename) { gutil.log('Created ' + gutil.colors.green(filename)); }))
            .pipe(browserSync.reload({ stream:true }));
    });
});

gulp.task('img', function () {
    var appList = glob.sync(PROJECT_APPS_PATH + '*/'),
        type = 'img';

    if (fs.existsSync(PROJECT_STATIC_PATH)) appList.push(PROJECT_STATIC_PATH);

    appList.forEach(function(folder) {
        appName = folder.match(/.+\/(.+)\/$/)[1];
        appImages = getConcatFiles(appName, type);
        if (appImages.length !== 0) {
            sprite = gulp.src(appImages)
                .pipe(filter(['*.png', '*.jpg', '*.gif', '!*-sprite.png']))
                .pipe(newer(getExistingFiles(appName, type) + appName + '-sprite.png'))
                .pipe(map(function(code, filename) { gutil.log('Use ' + gutil.colors.yellow(filename)); }))
                .pipe(spritesmith({
                    imgName: appName + '-sprite.png',
                    imgPath: '../img/' + appName + '-sprite.png',
                    cssName: appName +'-sprite.css',
                    algorithm: 'binary-tree',
                    cssOpts: {
                        cssClass: function (item) {
                            return '.' + item.name;
                        }
                    }
                }));

            sprite.img
                .pipe(gulp.dest(getExistingFiles(appName, type)))
                .pipe(map(function(code, filename) { gutil.log('Created ' + gutil.colors.green(filename)); }));

            var pathSource = getExistingFiles(appName, type);
            path = pathSource.substr(0, pathSource.length - 4) + 'css/';

            sprite.css
                .pipe(gulp.dest(path))
                .pipe(map(function(code, filename) { gutil.log('Created ' + gutil.colors.green(filename)); }));
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
            .pipe(filter(['*.html', '*.jinja2']))
            //.pipe(map(function(code, filename) { gutil.log(gutil.colors.green(filename)); }))
            .pipe(browserSync.reload({ stream:true }));
    });
});

gulp.task('watch', function () {

    // Check isseu at https://github.com/floatdrop/gulp-watch/issues/110
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

        watch(watchFiles, { name: type })
            //.pipe(map(function(code, filename) { gutil.log(gutil.colors.green(filename)); }))
            .on('data', function () { gulp.start(type); })
            .on('ready', function() {
                gutil.log(gutil.colors.cyan(type), 'is watching ' + ' files...');
        });
    });
});

gulp.task('default', ['watch', 'browser-sync']);