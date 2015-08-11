// Code to bind the JQuery UI datepicker to the AngularJS text input control
// Tried several options, but the one from
// http://stackoverflow.com/questions/18144142/jquery-ui-datepicker-with-angularjs
// is the one that worked, and also the one that seems to be the most
// generic one.
var directives = angular.module('directives', []);
directives.directive('datepicker', function() {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function(scope, element, attrs, ngModelCtrl) {
            $(element).datepicker({
                dateFormat: 'yy-mm-dd',
                onSelect: function(date) {
                    var ngModelName = this.attributes['ng-model'].value;

                    // if value for the specified ngModel is a property of
                    // another object on the scope
                    if (ngModelName.indexOf(".") != -1) {
                        var objAttributes = ngModelName.split(".");
                        var lastAttribute = objAttributes.pop();
                        var partialObjString = objAttributes.join(".");
                        var partialObj = eval("scope." + partialObjString);

                        partialObj[lastAttribute] = date;
                    }
                    // if value for the specified ngModel is directly on the scope
                    else {
                        scope[ngModelName] = date;
                    }
                    scope.$apply();
                }

            });
        }
    };
});

<!-- CODE - Angular modules/controllers. -->

// LOGIN
var loginModule = angular.module('Login', []);
loginModule.controller("LoginController", function ($scope, $rootScope, $http) {
        $scope.login = function () {
            $scope.dataLoading = true;
            var responsePromise = $http.get("/brain/login/" + $scope.username + "/" + $scope.password);
            $scope.password = '';  // clear the password field, so that it is empty after logout
            responsePromise.success(function(data, status, headers, config) {
                if (data == "True") {
                    $rootScope.loggedIn = true;
                } else {
                    alert("Login failed");
                }
                $scope.dataLoading = false;
            });
            responsePromise.error(function(data, status, headers, config) {
                alert("Could not verify credentials!");
                $scope.dataLoading = false;
            });
        };
    });

// MENU BAR
var menuModule = angular.module('MenuBar', []);
menuModule.controller("MenuController", function ($scope, $rootScope) {
        $scope.logout = function() {
            $rootScope.loggedIn = false;
        }
        $scope.users = function() {
            $rootScope.activePanel='users';
            $scope.userActive='menuItemActive';
            delete $scope.logActive;
            delete $scope.testActive;
            delete $scope.bankActive;
            delete $scope.gatekeeperActive;
        }
        $scope.logs = function() {
            $rootScope.activePanel='logs';
            $scope.logActive='menuItemActive';
            delete $scope.userActive;
            delete $scope.testActive;
            delete $scope.bankActive;
            delete $scope.gatekeeperActive;
        }
        $scope.bank = function() {
            $rootScope.activePanel='bank';
            $scope.bankActive='menuItemActive';
            delete $scope.logActive;
            delete $scope.userActive;
            delete $scope.gatekeeperActive;
            delete $scope.testActive;
        }
        $scope.gatekeeper = function() {
            $rootScope.activePanel='gatekeeper';
            $scope.gatekeeperActive='menuItemActive';
            delete $scope.logActive;
            delete $scope.userActive;
            delete $scope.bankActive;
            delete $scope.testActive;
        }
        $scope.test = function() {
            $rootScope.activePanel='test';
            $scope.testActive='menuItemActive';
            delete $scope.logActive;
            delete $scope.userActive;
            delete $scope.bankActive;
            delete $scope.gatekeeperActive;
        }
    });

// USER PANEL
var userModule = angular.module('User', []);
userModule.controller("UserController", function($scope, $http) {
        // USER LIST
        $scope.loadUserList = function() {
            //alert("load users");
            var responsePromise = $http.get("/brain/user/all");
            responsePromise.success(function(data, status, headers, config) {
                $scope.userListData = data.users;
                $scope.clearSelection();
            });
            responsePromise.error(function(data, status, headers, config) {
                alert("Could not load user list!");
            });
        }
        // Select a user: lazy load the details
        $scope.selectUser = function(item) {
            $scope.selectedUser = item;
            var responsePromise = $http.get("/brain/user/" + $scope.selectedUser.id + "/phonenumbers");
            responsePromise.success(function(data, status, headers, config) {
                $scope.selectedUser.phonenumbers = data.phonenumbers;
            });
            responsePromise.error(function(data, status, headers, config) {
                alert("Could not load user details!");
                $scope.clearSelectionAndReload();
            });

        }
        $scope.deleteUser = function(item) {
            var responsePromise = $http.get("/brain/user/delete/" + item.id);
            responsePromise.success(function(data, status, headers, config) {
                $scope.clearSelectionAndReload();
            });
            responsePromise.error(function(data, status, headers, config) {
                alert("Could not delete user!");
                $scope.clearSelectionAndReload();
            });
        }

        // USER DETAILS FORM
        $scope.newUser = function(item) {
            $scope.clearSelection();
            // id -1 signals the server to create a new user
            $scope.selectedUser = { "id": -1 };
        }
        $scope.saveUserDetails = function() {
            if ($scope.selectedUser.member == undefined) {
                $scope.selectedUser.member = false;
            }
            var responsePromise = $http.get("/brain/user/update/" +
                                            $scope.selectedUser.id + "/" +
                                            $scope.selectedUser.firstname + "/" +
                                            $scope.selectedUser.lastname + "/" +
                                            $scope.selectedUser.member);
            responsePromise.success(function(data, status, headers, config) {
                $scope.selectUser($scope.selectedUser);  // reload user details & refresh screen
            });
            responsePromise.error(function(data, status, headers, config) {
                alert("Could not save user!");
                $scope.clearSelection();
            });
            $scope.loadUserList();
            $http.get("/brain/logs/add/groundcontrol/none/Update user " + $scope.selectedUser.id + " (" +
                      $scope.selectedUser.firstname + " " + $scope.selectedUser.lastname +")");

        }
        $scope.clearSelectionAndReload = function() {
            $scope.loadUserList();
            $scope.clearSelection();
        }
        $scope.clearSelection = function() {
            // remove any previously selected user from the scope
            delete $scope.selectedUser;
        }

        $scope.refreshSelectedUser = function() {
            $scope.selectUser($scope.selectedUser);
        }
        $scope.newPhoneNumber = function() {
            $scope.newPhoneNumber = {};
        }
        $scope.deletePhonenumber = function(item) {
           var responsePromise = $http.get("/brain/user/deletephonenumber/" + item.id);
            responsePromise.success(function(data, status, headers, config) {
               $scope.refreshSelectedUser();
            });
        }
        $scope.savePhonenumbers = function() {
            $scope.selectedUser.phonenumbers.forEach(function(phonenumber) {
                                   $http.get("/brain/user/updatephonenumber/" +
                                            phonenumber.id + "/" +
                                            phonenumber.user_id + "/" +
                                            phonenumber.phonenumber + "/" +
                                            phonenumber.cellphone);
            });
            if (($scope.newphonenumber != undefined) &&
                ($scope.newphonenumber.phonenumber != "")) {
               if ($scope.newphonenumber.cellphone == undefined) {
                    $scope.newphonenumber.cellphone = false;
               }
               $http.get("/brain/user/updatephonenumber/-1/" +
                        $scope.selectedUser.id + "/" +
                        $scope.newphonenumber.phonenumber + "/" +
                        $scope.newphonenumber.cellphone);

                        delete $scope.newphonenumber;
                        $scope.refreshSelectedUser();
            }
        }

        $scope.saveUsernamePassword = function(item) {
            $http.get("/brain/user/"  + $scope.selectedUser.id + "/updatepassword/" +
                       $scope.selectedUser.username + "/" + $scope.selectedUser.password);
        }
        $scope.loadUserList();
    } );

// LOGS
var logModule = angular.module('Logs', []);
logModule.controller("LogController", function ($scope, $http) {
        $scope.getLogs = function() {
            var responsePromise = $http.get("/brain/logs/from/" + $scope.fromTS + "/to/" + $scope.toTS);
            responsePromise.success(function(data, status, headers, config) {
                $scope.logs = data.logEntries;
            });
        }
    });

// TRANSACTIONS
var bankTransactionModule = angular.module('Transaction', []);
bankTransactionModule.controller("TransactionController", function ($scope, $http) {
        $scope.getTransactions = function() {
            var responsePromise = $http.get("/brain/banktransactions/from/" + $scope.tFromTS + "/to/" + $scope.tToTS);
            responsePromise.success(function(data, status, headers, config) {
                $scope.transactions = data.transactions;
            });
        }
    });

// GATEKEEPER
var gatekeeperModule = angular.module('Gatekeeper', []);
gatekeeperModule.controller("GatekeeperController", function ($scope, $http) {
        $scope.newSchedule = function() {
            $scope.newSchedule = {};
        }
        $scope.modifySchedule = function() {
            var responsePromise = $http.get("/brain/access/schedules/all");
            responsePromise.success(function(data, status, headers, config) {
                $scope.schedules = data.schedules;
            });
        }
        $scope.deleteSchedule = function(item) {
           var responsePromise = $http.get("/brain/access/schedules/delete/" + item.id);
           responsePromise.success(function(data, status, headers, config) {
                $scope.modifySchedule();
           });
        }
        $scope.saveSchedules = function() {
            if (($scope.newSchedule != undefined) &&
                ($scope.newSchedule.day != "") &&
                ($scope.newSchedule.starttime != "") &&
                ($scope.newSchedule.endtime != "")) {
               $http.get("/brain/access/schedules/add/" +
                        $scope.newSchedule.day + "/" +
                        $scope.newSchedule.starttime + "/" +
                        $scope.newSchedule.endtime);

                        delete $scope.newSchedule;
                        $scope.modifySchedule();
            }
        }
        $scope.modifySchedule();
    });

// TEST
var testModule = angular.module('Test', []);
testModule.controller("TestController", function ($scope, $http) {
        $scope.addGatekeeperLog = function() {
            // Mock test: retrieve the list of users; if the given phone number
            // is in the list, we send a success message; if not, we send a failure message
            var responsePromise = $http.get("/brain/access/gsmnumbers/all");
            responsePromise.success(function(data, status, headers, config) {
                var phoneNumbers = data.split("\n");
                if (phoneNumbers.indexOf($scope.phoneNumber) >= 0) {
                    $http.get("/brain/logs/add/gatekeeper/" + $scope.phoneNumber +",TRUE" + "/call from: " + $scope.phoneNumber + "; gate OPENED");
                } else {
                    $http.get("/brain/logs/add/gatekeeper/" + $scope.phoneNumber +",FALSE" + "/call from: " + $scope.phoneNumber + "; gate NOT OPENED");
                }
            });
        }
        $scope.addDooropenerLog = function() {
            // Mock test: retrieve the list of users; if the given phone number
            // is in the list, we send a success message; if not, we send a failure message
            $http.get("/brain/logs/add/dooropener/" + $scope.badgeNumber +",TRUE" + "/access attempt from: " + $scope.badgeNumber + "; door OPENED");
        }
    });

// APPLICATION
angular.module('GroundControl', [
    'Login',
    'MenuBar',
    'User',
    'Test',
    'Logs',
    'Transaction',
    'Gatekeeper',
    'directives'
]);
