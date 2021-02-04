<?php
    use PHPMailer\PHPMailer\PHPMailer;
    use PHPMailer\PHPMailer\SMTP;
    use PHPMailer\PHPMailer\Exception;

    require('/var/www/html/vendor/autoload.php');
    
    function sendEmail($toAddress, $subject, $htmlBody, $body)
    {
        $sendEmail_result = json_decode('{}');
        
        $mail = new PHPMailer(true);
        
        try
        {
            $mail->SMTPOptions = array(
                'ssl' => array(
                    'verify_peer' => false,
                    'verify_peer_name' => false,
                    'allow_self_signed' => true
                )
            );
            
#            $mail->SMTPDebug = SMTP::DEBUG_SERVER;
            $mail->isSMTP();
            $mail->Host       = 'smtp.gmail.com';
            $mail->SMTPAuth   = true;
            $mail->Username   = '';
            $mail->Password   = '';
            $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS; 
            $mail->Port       = 587;
            
            $mail->setFrom('', '');
            $mail->addAddress($toAddress);
            
            $mail->isHTML(true);
            $mail->Subject = $subject;
            $mail->Body    = $htmlBody;
            $mail->AltBody = $body;
            
            $mail->send();
            $sendEmail_result->status = 'Success';
            return $sendEmail_result;
        }
        catch (Exception $e)
        {
            $sendEmail_result->status = 'Error';
            $sendEmail_result->error = $mail->ErrorInfo;
            return $sendEmail_result;
        }
    }
?>
