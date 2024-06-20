//
//  UIAlertController+Extensions.swift
//  Soundscape
//
//  Copyright (c) Microsoft Corporation.
//  Licensed under the MIT License.
//

import Foundation

enum MailClient: String, CaseIterable {
    
    // TODO: Add Mail Clients that you would like to support
    // These applications must also be defined in 'Queried URL Schemes' in Info.plist
    
    case gmail
    case outlook
    case defaultMail
    
    var localizedTitle: String {
        // TODO: Return a localized title string for each mail client
        
        switch self {
            case .gmail: return GDLocalizationUnnecessary("Gmail")
            case .outlook: return GDLocalizationUnnecessary("Outlook")
            case .defaultMail: return GDLocalizationUnnecessary("Mail app")
        }
    }
    
    func url(email: String, subject: String) -> URL? {
        let deviceInfo = "iOS \(UIDevice.current.systemVersion), \(UIDevice.current.modelName), \(LocalizationContext.currentAppLocale.identifierHyphened), v\(AppContext.appVersion).\(AppContext.appBuild)"
        let escapedSubject = "\(subject) (\(deviceInfo))".addingPercentEncoding(withAllowedCharacters: NSCharacterSet.urlQueryAllowed) ?? GDLocalizedString("settings.feedback.subject")
        
        // TODO: Return appropriate URL for each mail client
        
        switch self {
            case .gmail: return URL(string: "googlegmail://co?to=\(Bundle.main.object(forInfoDictionaryKey: "FeedbackMail") as! String)&subject=\(escapedSubject)")
            case .outlook: return URL(string: "ms-outlook://compose?to=\(Bundle.main.object(forInfoDictionaryKey: "FeedbackMail") as! String)&subject=\(escapedSubject)")
            case .defaultMail: return URL(string: "mailto:\(Bundle.main.object(forInfoDictionaryKey: "FeedbackMail") as! String)?subject=\(escapedSubject)")
        }
    }
}

extension UIAlertController {
    /// Create and return a `UIAlertController` that is able to send an email with external email clients
    convenience init(email: String, subject: String, preferredStyle: UIAlertController.Style, handler: ((MailClient?) -> Void)? = nil) {

        // Create alert actions from mail clients
        let actions = MailClient.allCases.compactMap { (client) -> UIAlertAction? in
            guard let url = client.url(email: email, subject: subject) else { return nil }
            return UIAlertAction(title: client.localizedTitle, url: url) {
                handler?(client)
            }
        }
        
        if actions.isEmpty {
            self.init(title: GDLocalizedString("general.error.error_occurred"),
                      message: GDLocalizedString("settings.feedback.no_mail_client_error"),
                      preferredStyle: .alert)
        } else {
            self.init(title: GDLocalizedString("settings.feedback.choose_email_app"),
                      message: nil,
                      preferredStyle: preferredStyle)
            
            actions.forEach({ action in
                self.addAction(action)
            })
        }
        
        self.addAction(UIAlertAction(title: GDLocalizedString("general.alert.cancel"), style: .cancel, handler: nil))
    }
}
