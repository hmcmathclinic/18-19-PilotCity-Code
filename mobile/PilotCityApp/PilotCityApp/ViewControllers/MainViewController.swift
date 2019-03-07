//
//  MainViewController.swift
//  PilotCityApp
//
//  Created by Selasi Jean Kwame Adedze on 2/7/19.
//  Copyright © 2019 PilotCity. All rights reserved.
//

import UIKit

class MainViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }
    
    @IBAction func didTapLogoutButton(_ sender: Any) {
        AuthProvider.Instance.logout()
        self.performSegue(withIdentifier: "logoutSegue", sender: nil)
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
