//
//  LoginViewController.swift
//  PilotCityApp
//
//  Created by Selasi Jean Kwame Adedze on 2/7/19.
//  Copyright © 2019 PilotCity. All rights reserved.
//

import UIKit

class LoginSignUpViewController: UIViewController {

    @IBOutlet weak var loginSignUpButton: UIButton!
    @IBOutlet weak var emailTextField: UITextField!
    @IBOutlet weak var passwordTextField: UITextField!
    var actionButtonTitle: String = ""
    override func viewDidLoad() {
        super.viewDidLoad()
        loginSignUpButton.setTitle(actionButtonTitle, for: .normal)
        // Do any additional setup after loading the view.
    }
    
    @IBAction func didTapCloseButton(_ sender: Any) {
        self.dismiss(animated: true, completion: nil)
    }
    
    @IBAction func didTapLoginButton(_ sender: Any) {
        if actionButtonTitle == "Login" {
            if emailTextField.text != "" && passwordTextField.text != ""{
                
                AuthProvider.Instance.login(withEmail: emailTextField.text!, password: passwordTextField.text!, loginHandler: { (message) in
                    
                    if message != nil{
                        self.alertTheUser(title: "Problem with Authentication", message: message!)
                        
                    }else{
                        self.emailTextField.text = ""
                        self.passwordTextField.text = ""
                        self.performSegue(withIdentifier: "loginSegue", sender: nil)
                    }
                })
            }else{
                alertTheUser(title: "Email And Password Are Required", message: "Please enter email and password in the text fields")
            }
        } else {
            if emailTextField.text != "" && passwordTextField.text != "" {
                AuthProvider.Instance.signUp(withEmail: emailTextField.text!, password: passwordTextField.text!, firstName: "", lastName: "", loginHandler: { (message) in
                    
                    if message != nil {
                        self.alertTheUser(title: "Problem With Creating A New User", message: message!);
                    } else {
                        self.emailTextField.text = "";
                        self.passwordTextField.text = "";
                        self.performSegue(withIdentifier: "loginSegue", sender: nil)
                    }
                });
            } else {
                alertTheUser(title: "Email And Password Are Required", message: "Please enter email and password in the text fields");
            }
        }
        
    }
    
    private func alertTheUser(title: String, message: String){
        let alert = UIAlertController(title: title, message: message, preferredStyle: .alert)
        let ok = UIAlertAction(title: "OK", style: .default, handler: nil)
        alert.addAction(ok)
        present(alert, animated: true, completion: nil)
    }
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
