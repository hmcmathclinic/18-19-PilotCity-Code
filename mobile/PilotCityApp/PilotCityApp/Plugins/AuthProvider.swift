//
//  File.swift
//  PilotCityApp
//
//  Created by Selasi Jean Kwame Adedze on 2/7/19.
//  Copyright © 2019 PilotCity. All rights reserved.
//

import Foundation
import Firebase
import FirebaseAuth
import SVProgressHUD

typealias LoginHandler = (_ msg: String?) -> Void

struct LoginErrorCode {
    
    static let INVALID_EMAIL = "Invalid Email Address. Please Provide a valid email address"
    static let WRONG_PASSWORD = "Wrong Password, Please Enter The Correct Password";
    static let PROBLEM_CONNECTING = "Problem Connecting To Database, Please Try Later";
    static let USER_NOT_FOUND = "User Not Found, Please Register";
    static let EMAIL_ALREADY_IN_USE = "Email Already In Use, Please Use Another Email";
    static let WEAK_PASSWORD = "Password Should Be At Least 6 Characters Long";
    
}

class AuthProvider{
    
    private static let _instance = AuthProvider()
    
    static var Instance: AuthProvider{
        return _instance
    }
    
    private init(){
        
    }
    
    func login(withEmail: String, password: String, loginHandler: LoginHandler?){
        SVProgressHUD.setDefaultMaskType(.black)
        SVProgressHUD.show()
        Auth.auth().signIn(withEmail: withEmail, password: password, completion: { (user, error) in
            
            if error != nil{
                self.handleErrors(err: error! as NSError, loginHandler: loginHandler)
                SVProgressHUD.dismiss()
            }else{
                loginHandler?(nil)
                SVProgressHUD.dismiss()
            }
            
        })
    }//sign in user to app
    
    func signUp(withEmail: String, password: String, firstName: String, lastName: String, loginHandler:LoginHandler?){
        Auth.auth().createUser(withEmail: withEmail, password: password) { (result, error) in
            if error != nil{
                self.handleErrors(err: error! as NSError, loginHandler: loginHandler)
            }else{
                if result?.user.uid != nil{
                    //store user to database
                    self.login(withEmail: withEmail, password: password, loginHandler: loginHandler)
                }
            }
        }
    }//sign up user
    
    func logout() -> Bool{
        
        if Auth.auth().currentUser != nil{
            do {
                try Auth.auth().signOut()
                return true
            } catch {
                return false
            }
        }
        return true
        
    }//logs user out of app
    
    private func handleErrors(err: NSError, loginHandler: LoginHandler?){
        
        if let errCode = AuthErrorCode(rawValue: err.code) {
            
            switch errCode {
                
            case .wrongPassword:
                loginHandler?(LoginErrorCode.WRONG_PASSWORD);
                break;
                
            case .invalidEmail:
                loginHandler?(LoginErrorCode.INVALID_EMAIL);
                break;
                
            case .userNotFound:
                loginHandler?(LoginErrorCode.USER_NOT_FOUND);
                break;
                
            case .emailAlreadyInUse:
                loginHandler?(LoginErrorCode.EMAIL_ALREADY_IN_USE);
                break;
                
            case .weakPassword:
                loginHandler?(LoginErrorCode.WEAK_PASSWORD);
                break;
                
            default:
                print(err.localizedDescription)
                loginHandler?(LoginErrorCode.PROBLEM_CONNECTING);
                break;
            }
        }
        
    }// handle potential sign in and login errors.
}//class

