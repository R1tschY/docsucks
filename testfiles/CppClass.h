#include <unordered_map>


namespace MyModule {

/**
 * a service locator for your services
 *
 * \code
 * struct AnswerService {
 *   virtual int getAnswer() { return 42; }
 * };
 * auto locator = ServiceLocator()
 * locator.set("TruthService", std::make_unique<AnswerService>())
 * std::cout << locator.get<AnswerService>("TruthService").getAnswer() << '\n';
 * \endcode
 *
 * \verbatim
 * 42
 * \endverbatim
 *
 * \code
 * std::cout << &locator.get<AnswerService>("TruthService") << '\n';
 * \endcode
 * \verbatim
 * 0
 * \endverbatim
 */
class ServiceLocator
{
public:
  ServiceLocator();



private:
  std::unordered_map<std::string, void*> services_;
};

} // namespace MyModule
