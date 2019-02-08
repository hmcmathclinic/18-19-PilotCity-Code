//
//  ViewController.swift
//  PilotCityApp
//
//  Created by Selasi Jean Kwame Adedze on 2/7/19.
//  Copyright © 2019 PilotCity. All rights reserved.
//

import UIKit

class WelcomeViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    @IBAction func didTapLoginButton(_ sender: Any) {
        let vc = self.storyboard?.instantiateViewController(withIdentifier: "loginSignUpVC") as! LoginSignUpViewController
        vc.actionButtonTitle = "Login"
        self.present(vc, animated: true, completion: nil)
    }
    @IBAction func didTapSignUpButton(_ sender: Any) {
        let vc = self.storyboard?.instantiateViewController(withIdentifier: "loginSignUpVC") as! LoginSignUpViewController
        vc.actionButtonTitle = "Sign up"
        self.present(vc, animated: true, completion: nil)
    }
    
}

